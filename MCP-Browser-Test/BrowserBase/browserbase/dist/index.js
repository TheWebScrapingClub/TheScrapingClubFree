#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListResourcesRequestSchema, ListToolsRequestSchema, ReadResourceRequestSchema, } from "@modelcontextprotocol/sdk/types.js";
import puppeteer from "puppeteer-core";
import { Browserbase } from "@browserbasehq/sdk";
// Environment variables configuration
const requiredEnvVars = {
    BROWSERBASE_API_KEY: process.env.BROWSERBASE_API_KEY,
    BROWSERBASE_PROJECT_ID: process.env.BROWSERBASE_PROJECT_ID,
};
// Validate required environment variables
Object.entries(requiredEnvVars).forEach(([name, value]) => {
    if (!value)
        throw new Error(`${name} environment variable is required`);
});
// 2. Global State
const browsers = new Map();
const consoleLogs = [];
const screenshots = new Map();
// 3. Helper Functions
async function createNewBrowserSession(sessionId) {
    const bb = new Browserbase({
        apiKey: process.env.BROWSERBASE_API_KEY,
    });
    const session = await bb.sessions.create({
        projectId: process.env.BROWSERBASE_PROJECT_ID,
    });
    const browser = await puppeteer.connect({
        browserWSEndpoint: session.connectUrl,
    });
    const page = (await browser.pages())[0];
    browsers.set(sessionId, { browser, page });
    // Set up console logging for this session
    page.on("console", (msg) => {
        const logEntry = `[Session ${sessionId}][${msg.type()}] ${msg.text()}`;
        consoleLogs.push(logEntry);
        server.notification({
            method: "notifications/cloud/message",
            params: { message: logEntry, type: "console_log" },
        });
    });
    return { browser, page };
}
// 4. Tool Definitions
const TOOLS = [
    {
        name: "browserbase_create_session",
        description: "Create a new cloud browser session using Browserbase",
        inputSchema: {
            type: "object",
            properties: {},
            required: [],
        },
    },
    {
        name: "browserbase_close_session",
        description: "Close a browser session on Browserbase",
        inputSchema: {
            type: "object",
            properties: {
                sessionId: { type: "string" },
            },
            required: ["sessionId"],
        },
    },
    {
        name: "browserbase_navigate",
        description: "Navigate to a URL",
        inputSchema: {
            type: "object",
            properties: {
                url: { type: "string" },
            },
            required: ["url"],
        },
    },
    {
        name: "browserbase_screenshot",
        description: "Take a screenshot of the current page or a specific element",
        inputSchema: {
            type: "object",
            properties: {
                name: { type: "string", description: "Name for the screenshot" },
                selector: {
                    type: "string",
                    description: "CSS selector for element to screenshot",
                },
                width: {
                    type: "number",
                    description: "Width in pixels (default: 800)",
                },
                height: {
                    type: "number",
                    description: "Height in pixels (default: 600)",
                },
            },
            required: ["name"],
        },
    },
    {
        name: "browserbase_click",
        description: "Click an element on the page",
        inputSchema: {
            type: "object",
            properties: {
                selector: {
                    type: "string",
                    description: "CSS selector for element to click",
                },
            },
            required: ["selector"],
        },
    },
    {
        name: "browserbase_fill",
        description: "Fill out an input field",
        inputSchema: {
            type: "object",
            properties: {
                selector: {
                    type: "string",
                    description: "CSS selector for input field",
                },
                value: { type: "string", description: "Value to fill" },
            },
            required: ["selector", "value"],
        },
    },
    {
        name: "browserbase_evaluate",
        description: "Execute JavaScript in the browser console",
        inputSchema: {
            type: "object",
            properties: {
                script: { type: "string", description: "JavaScript code to execute" },
            },
            required: ["script"],
        },
    },
    {
        name: "browserbase_get_content",
        description: "Extract all content from the current page",
        inputSchema: {
            type: "object",
            properties: {
                selector: {
                    type: "string",
                    description: "Optional CSS selector to get content from specific elements (default: returns whole page)",
                },
            },
            required: [],
        },
    }
];
// 5. Tool Handler Implementation
async function handleToolCall(name, args) {
    // Only auto-create sessions for tools OTHER than create_session
    const defaultSession = !["browserbase_create_session"].includes(name)
        ? browsers.get(args.sessionId) ||
            (await createNewBrowserSession(args.sessionId))
        : null;
    switch (name) {
        case "browserbase_close_session":
            await defaultSession.browser.close();
            browsers.delete(args.sessionId);
            return {
                content: [{ type: "text", text: "Closed session" }],
            };
        case "browserbase_create_session":
            try {
                // Check if session already exists
                if (browsers.has(args.sessionId)) {
                    return {
                        content: [
                            {
                                type: "text",
                                text: "Session already exists",
                            },
                        ],
                        isError: false,
                    };
                }
                await createNewBrowserSession(args.sessionId);
                return {
                    content: [
                        {
                            type: "text",
                            text: "Created new browser session",
                        },
                    ],
                    isError: false,
                };
            }
            catch (error) {
                return {
                    content: [
                        {
                            type: "text",
                            text: `Failed to create browser session: ${error.message}`,
                        },
                    ],
                    isError: true,
                };
            }
        case "browserbase_navigate":
            await defaultSession.page.goto(args.url);
            return {
                content: [
                    {
                        type: "text",
                        text: `Navigated to ${args.url}`,
                    },
                ],
                isError: false,
            };
        case "browserbase_screenshot": {
            const width = args.width ?? 800;
            const height = args.height ?? 600;
            await defaultSession.page.setViewport({ width, height });
            const screenshot = await (args.selector
                ? (await defaultSession.page.$(args.selector))?.screenshot({ encoding: "base64" })
                : defaultSession.page.screenshot({
                    encoding: "base64",
                    fullPage: false,
                }));
            if (!screenshot) {
                return {
                    content: [
                        {
                            type: "text",
                            text: args.selector
                                ? `Element not found: ${args.selector}`
                                : "Screenshot failed",
                        },
                    ],
                    isError: true,
                };
            }
            screenshots.set(args.name, screenshot);
            server.notification({
                method: "notifications/resources/list_changed",
            });
            return {
                content: [
                    {
                        type: "text",
                        text: `Screenshot '${args.name}' taken at ${width}x${height}`,
                    },
                    {
                        type: "image",
                        data: screenshot,
                        mimeType: "image/png",
                    },
                ],
                isError: false,
            };
        }
        case "browserbase_click":
            try {
                await defaultSession.page.click(args.selector);
                return {
                    content: [
                        {
                            type: "text",
                            text: `Clicked: ${args.selector}`,
                        },
                    ],
                    isError: false,
                };
            }
            catch (error) {
                return {
                    content: [
                        {
                            type: "text",
                            text: `Failed to click ${args.selector}: ${error.message}`,
                        },
                    ],
                    isError: true,
                };
            }
        case "browserbase_fill":
            try {
                await defaultSession.page.waitForSelector(args.selector);
                await defaultSession.page.type(args.selector, args.value);
                return {
                    content: [
                        {
                            type: "text",
                            text: `Filled ${args.selector} with: ${args.value}`,
                        },
                    ],
                    isError: false,
                };
            }
            catch (error) {
                return {
                    content: [
                        {
                            type: "text",
                            text: `Failed to fill ${args.selector}: ${error.message}`,
                        },
                    ],
                    isError: true,
                };
            }
        case "browserbase_evaluate":
            try {
                const result = await defaultSession.page.evaluate((script) => {
                    const logs = [];
                    const originalConsole = { ...console };
                    ["log", "info", "warn", "error"].forEach((method) => {
                        console[method] = (...args) => {
                            logs.push(`[${method}] ${args.join(" ")}`);
                            originalConsole[method](...args);
                        };
                    });
                    try {
                        const result = eval(script);
                        Object.assign(console, originalConsole);
                        return { result, logs };
                    }
                    catch (error) {
                        Object.assign(console, originalConsole);
                        throw error;
                    }
                }, args.script);
                return {
                    content: [
                        {
                            type: "text",
                            text: `Execution result:\n${JSON.stringify(result.result, null, 2)}\n\nConsole output:\n${result.logs.join("\n")}`,
                        },
                    ],
                    isError: false,
                };
            }
            catch (error) {
                return {
                    content: [
                        {
                            type: "text",
                            text: `Script execution failed: ${error.message}`,
                        },
                    ],
                    isError: true,
                };
            }
        case "browserbase_get_json":
            try {
                const result = await defaultSession.page.evaluate((selector) => {
                    // Helper function to find JSON in text
                    function extractJSON(text) {
                        const jsonObjects = [];
                        let braceCount = 0;
                        let start = -1;
                        for (let i = 0; i < text.length; i++) {
                            if (text[i] === "{") {
                                if (braceCount === 0)
                                    start = i;
                                braceCount++;
                            }
                            else if (text[i] === "}") {
                                braceCount--;
                                if (braceCount === 0 && start !== -1) {
                                    try {
                                        const jsonStr = text.slice(start, i + 1);
                                        const parsed = JSON.parse(jsonStr);
                                        jsonObjects.push(parsed);
                                    }
                                    catch (e) {
                                        // Invalid JSON, continue searching
                                    }
                                }
                            }
                        }
                        return jsonObjects;
                    }
                    // Get all text content based on selector or full page
                    const elements = selector
                        ? Array.from(document.querySelectorAll(selector))
                        : [document.body];
                    const results = {
                        // Look for JSON in text content
                        textContent: elements.flatMap((el) => extractJSON(el.textContent || "")),
                        // Look for JSON in script tags
                        scriptTags: Array.from(document.getElementsByTagName("script")).flatMap((script) => {
                            try {
                                if (script.type === "application/json") {
                                    return [JSON.parse(script.textContent || "")];
                                }
                                return extractJSON(script.textContent || "");
                            }
                            catch (e) {
                                return [];
                            }
                        }),
                        // Look for JSON in meta tags
                        metaTags: Array.from(document.getElementsByTagName("meta")).flatMap((meta) => {
                            try {
                                const content = meta.getAttribute("content") || "";
                                return extractJSON(content);
                            }
                            catch (e) {
                                return [];
                            }
                        }),
                        // Look for JSON-LD
                        jsonLd: Array.from(document.querySelectorAll('script[type="application/ld+json"]')).flatMap((script) => {
                            try {
                                return [JSON.parse(script.textContent || "")];
                            }
                            catch (e) {
                                return [];
                            }
                        }),
                    };
                    return results;
                }, args.selector);
                return {
                    content: [
                        {
                            type: "text",
                            text: `Found JSON content:\n${JSON.stringify(result, null, 2)}`,
                        },
                    ],
                    isError: false,
                };
            }
            catch (error) {
                return {
                    content: [
                        {
                            type: "text",
                            text: `Failed to extract JSON: ${error.message}`,
                        },
                    ],
                    isError: true,
                };
            }
        case "browserbase_get_content":
            try {
                let content;
                if (args.selector) {
                    // If selector is provided, get content from specific elements
                    content = await defaultSession.page.evaluate((selector) => {
                        const elements = document.querySelectorAll(selector);
                        return Array.from(elements).map((el) => el.textContent || "");
                    }, args.selector);
                }
                else {
                    // If no selector is provided, get content from the whole page
                    content = await defaultSession.page.evaluate(() => {
                        return Array.from(document.querySelectorAll("*")).map((el) => el.textContent || "");
                    });
                }
                return {
                    content: [
                        {
                            type: "text",
                            text: `Extracted content:\n${JSON.stringify(content, null, 2)}`,
                        },
                    ],
                    isError: false,
                };
            }
            catch (error) {
                return {
                    content: [
                        {
                            type: "text",
                            text: `Failed to extract content: ${error.message}`,
                        },
                    ],
                    isError: true,
                };
            }
        default:
            return {
                content: [
                    {
                        type: "text",
                        text: `Unknown tool: ${name}`,
                    },
                ],
                isError: true,
            };
    }
}
// 6. Server Setup and Configuration
const server = new Server({
    name: "example-servers/browserbase",
    version: "0.1.0",
}, {
    capabilities: {
        resources: {},
        tools: {},
    },
});
// 7. Request Handlers
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
    resources: [
        {
            uri: "console://logs",
            mimeType: "text/plain",
            name: "Browser console logs",
        },
        ...Array.from(screenshots.keys()).map((name) => ({
            uri: `screenshot://${name}`,
            mimeType: "image/png",
            name: `Screenshot: ${name}`,
        })),
    ],
}));
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    const uri = request.params.uri.toString();
    if (uri === "console://logs") {
        return {
            contents: [
                {
                    uri,
                    mimeType: "text/plain",
                    text: consoleLogs.join("\n"),
                },
            ],
        };
    }
    if (uri.startsWith("screenshot://")) {
        const name = uri.split("://")[1];
        const screenshot = screenshots.get(name);
        if (screenshot) {
            return {
                contents: [
                    {
                        uri,
                        mimeType: "image/png",
                        blob: screenshot,
                    },
                ],
            };
        }
    }
    throw new Error(`Resource not found: ${uri}`);
});
server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: TOOLS,
}));
server.setRequestHandler(CallToolRequestSchema, async (request) => handleToolCall(request.params.name, request.params.arguments ?? {}));
// 8. Server Initialization
async function runServer() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
}
runServer().catch(console.error);
