# Browserbase MCP Server

![cover](../assets/browserbase-mcp.png)

## Get Started

1. Run `npm install` to install the necessary dependencies, then run `npm run build` to get `dist/index.js`.

2. Set up your Claude Desktop configuration to use the server.  

```json
{
  "mcpServers": {
    "browserbase": {
      "command": "node",
      "args": ["path/to/mcp-server-browserbase/browserbase/dist/index.js"],
      "env": {
        "BROWSERBASE_API_KEY": "<YOUR_BROWSERBASE_API_KEY>",
        "BROWSERBASE_PROJECT_ID": "<YOUR_BROWSERBASE_PROJECT_ID>"
      }
    }
  }
}
```

3. Restart your Claude Desktop app and you should see the tools available clicking the 🔨 icon.

4. Start using the tools! Below is an image of Claude closing a browser session.

<p align="center">
  <img src="../assets/browserbase-demo.png" alt="demo" width="600"/>
</p>


## Tools

### Browserbase API

- **browserbase_create_session**

  - Create a new cloud browser session using Browserbase
  - No required inputs

- **browserbase_navigate**

  - Navigate to any URL in the browser
  - Input: `url` (string)

- **browserbase_screenshot**

  - Capture screenshots of the entire page or specific elements
  - Inputs:
    - `name` (string, required): Name for the screenshot
    - `selector` (string, optional): CSS selector for element to screenshot
    - `width` (number, optional, default: 800): Screenshot width
    - `height` (number, optional, default: 600): Screenshot height

- **browserbase_click**

  - Click elements on the page
  - Input: `selector` (string): CSS selector for element to click

- **browserbase_fill**

  - Fill out input fields
  - Inputs:
    - `selector` (string): CSS selector for input field
    - `value` (string): Value to fill

- **browserbase_evaluate**

  - Execute JavaScript in the browser console
  - Input: `script` (string): JavaScript code to execute

- **browserbase_get_content**

  - Extract all content from the current page
  - Input: `selector` (string, optional): CSS selector to get content from specific elements

- **browserbase_parallel_sessions**
  - Create multiple browser sessions and navigate to different URLs
  - Input: `sessions` (array): Array of objects containing:
    - `url` (string): URL to navigate to
    - `id` (string): Session identifier

### Resources

The server provides access to two types of resources:

1. **Console Logs** (`console://logs`)

   - Browser console output in text format
   - Includes all console messages from the browser

2. **Screenshots** (`screenshot://<name>`)
   - PNG images of captured screenshots
   - Accessible via the screenshot name specified during capture

## Key Features

- Cloud browser automation
- Web data extraction
- Console log monitoring
- Screenshot capabilities
- JavaScript execution
- Basic web interaction (navigation, clicking, form filling)

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
