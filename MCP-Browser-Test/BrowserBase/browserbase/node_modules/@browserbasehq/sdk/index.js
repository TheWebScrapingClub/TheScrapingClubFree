"use strict";
// File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var _a;
Object.defineProperty(exports, "__esModule", { value: true });
exports.fileFromPath = exports.toFile = exports.UnprocessableEntityError = exports.PermissionDeniedError = exports.InternalServerError = exports.AuthenticationError = exports.BadRequestError = exports.RateLimitError = exports.ConflictError = exports.NotFoundError = exports.APIUserAbortError = exports.APIConnectionTimeoutError = exports.APIConnectionError = exports.APIError = exports.BrowserbaseError = exports.Browserbase = void 0;
const Errors = __importStar(require("./error.js"));
const Uploads = __importStar(require("./uploads.js"));
const Core = __importStar(require("./core.js"));
const API = __importStar(require("./resources/index.js"));
/**
 * API Client for interfacing with the Browserbase API.
 */
class Browserbase extends Core.APIClient {
    /**
     * API Client for interfacing with the Browserbase API.
     *
     * @param {string | undefined} [opts.apiKey=process.env['BROWSERBASE_API_KEY'] ?? undefined]
     * @param {string} [opts.baseURL=process.env['BROWSERBASE_BASE_URL'] ?? https://api.browserbase.com] - Override the default base URL for the API.
     * @param {number} [opts.timeout=1 minute] - The maximum amount of time (in milliseconds) the client will wait for a response before timing out.
     * @param {number} [opts.httpAgent] - An HTTP agent used to manage HTTP(s) connections.
     * @param {Core.Fetch} [opts.fetch] - Specify a custom `fetch` function implementation.
     * @param {number} [opts.maxRetries=2] - The maximum number of times the client will retry a request.
     * @param {Core.Headers} opts.defaultHeaders - Default headers to include with every request to the API.
     * @param {Core.DefaultQuery} opts.defaultQuery - Default query parameters to include with every request to the API.
     */
    constructor({ baseURL = Core.readEnv('BROWSERBASE_BASE_URL'), apiKey = Core.readEnv('BROWSERBASE_API_KEY'), ...opts } = {}) {
        if (apiKey === undefined) {
            throw new Errors.BrowserbaseError("The BROWSERBASE_API_KEY environment variable is missing or empty; either provide it, or instantiate the Browserbase client with an apiKey option, like new Browserbase({ apiKey: 'My API Key' }).");
        }
        const options = {
            apiKey,
            ...opts,
            baseURL: baseURL || `https://api.browserbase.com`,
        };
        super({
            baseURL: options.baseURL,
            timeout: options.timeout ?? 60000 /* 1 minute */,
            httpAgent: options.httpAgent,
            maxRetries: options.maxRetries,
            fetch: options.fetch,
        });
        this.contexts = new API.Contexts(this);
        this.extensions = new API.Extensions(this);
        this.projects = new API.Projects(this);
        this.sessions = new API.Sessions(this);
        this._options = options;
        this.apiKey = apiKey;
    }
    defaultQuery() {
        return this._options.defaultQuery;
    }
    defaultHeaders(opts) {
        return {
            ...super.defaultHeaders(opts),
            ...this._options.defaultHeaders,
        };
    }
    authHeaders(opts) {
        return { 'X-BB-API-Key': this.apiKey };
    }
}
exports.Browserbase = Browserbase;
_a = Browserbase;
Browserbase.Browserbase = _a;
Browserbase.DEFAULT_TIMEOUT = 60000; // 1 minute
Browserbase.BrowserbaseError = Errors.BrowserbaseError;
Browserbase.APIError = Errors.APIError;
Browserbase.APIConnectionError = Errors.APIConnectionError;
Browserbase.APIConnectionTimeoutError = Errors.APIConnectionTimeoutError;
Browserbase.APIUserAbortError = Errors.APIUserAbortError;
Browserbase.NotFoundError = Errors.NotFoundError;
Browserbase.ConflictError = Errors.ConflictError;
Browserbase.RateLimitError = Errors.RateLimitError;
Browserbase.BadRequestError = Errors.BadRequestError;
Browserbase.AuthenticationError = Errors.AuthenticationError;
Browserbase.InternalServerError = Errors.InternalServerError;
Browserbase.PermissionDeniedError = Errors.PermissionDeniedError;
Browserbase.UnprocessableEntityError = Errors.UnprocessableEntityError;
Browserbase.toFile = Uploads.toFile;
Browserbase.fileFromPath = Uploads.fileFromPath;
exports.BrowserbaseError = Errors.BrowserbaseError, exports.APIError = Errors.APIError, exports.APIConnectionError = Errors.APIConnectionError, exports.APIConnectionTimeoutError = Errors.APIConnectionTimeoutError, exports.APIUserAbortError = Errors.APIUserAbortError, exports.NotFoundError = Errors.NotFoundError, exports.ConflictError = Errors.ConflictError, exports.RateLimitError = Errors.RateLimitError, exports.BadRequestError = Errors.BadRequestError, exports.AuthenticationError = Errors.AuthenticationError, exports.InternalServerError = Errors.InternalServerError, exports.PermissionDeniedError = Errors.PermissionDeniedError, exports.UnprocessableEntityError = Errors.UnprocessableEntityError;
exports.toFile = Uploads.toFile;
exports.fileFromPath = Uploads.fileFromPath;
(function (Browserbase) {
    Browserbase.Contexts = API.Contexts;
    Browserbase.Extensions = API.Extensions;
    Browserbase.Projects = API.Projects;
    Browserbase.Sessions = API.Sessions;
})(Browserbase || (exports.Browserbase = Browserbase = {}));
exports = module.exports = Browserbase;
exports.default = Browserbase;
//# sourceMappingURL=index.js.map