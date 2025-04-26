import * as Errors from "./error.js";
import * as Uploads from "./uploads.js";
import { type Agent } from "./_shims/index.js";
import * as Core from "./core.js";
import * as API from "./resources/index.js";
export interface ClientOptions {
    /**
     * Your [Browserbase API Key](https://www.browserbase.com/settings).
     */
    apiKey?: string | undefined;
    /**
     * Override the default base URL for the API, e.g., "https://api.example.com/v2/"
     *
     * Defaults to process.env['BROWSERBASE_BASE_URL'].
     */
    baseURL?: string | null | undefined;
    /**
     * The maximum amount of time (in milliseconds) that the client should wait for a response
     * from the server before timing out a single request.
     *
     * Note that request timeouts are retried by default, so in a worst-case scenario you may wait
     * much longer than this timeout before the promise succeeds or fails.
     */
    timeout?: number;
    /**
     * An HTTP agent used to manage HTTP(S) connections.
     *
     * If not provided, an agent will be constructed by default in the Node.js environment,
     * otherwise no agent is used.
     */
    httpAgent?: Agent;
    /**
     * Specify a custom `fetch` function implementation.
     *
     * If not provided, we use `node-fetch` on Node.js and otherwise expect that `fetch` is
     * defined globally.
     */
    fetch?: Core.Fetch | undefined;
    /**
     * The maximum number of times that the client will retry a request in case of a
     * temporary failure, like a network error or a 5XX error from the server.
     *
     * @default 2
     */
    maxRetries?: number;
    /**
     * Default headers to include with every request to the API.
     *
     * These can be removed in individual requests by explicitly setting the
     * header to `undefined` or `null` in request options.
     */
    defaultHeaders?: Core.Headers;
    /**
     * Default query parameters to include with every request to the API.
     *
     * These can be removed in individual requests by explicitly setting the
     * param to `undefined` in request options.
     */
    defaultQuery?: Core.DefaultQuery;
}
/**
 * API Client for interfacing with the Browserbase API.
 */
export declare class Browserbase extends Core.APIClient {
    apiKey: string;
    private _options;
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
    constructor({ baseURL, apiKey, ...opts }?: ClientOptions);
    contexts: API.Contexts;
    extensions: API.Extensions;
    projects: API.Projects;
    sessions: API.Sessions;
    protected defaultQuery(): Core.DefaultQuery | undefined;
    protected defaultHeaders(opts: Core.FinalRequestOptions): Core.Headers;
    protected authHeaders(opts: Core.FinalRequestOptions): Core.Headers;
    static Browserbase: typeof Browserbase;
    static DEFAULT_TIMEOUT: number;
    static BrowserbaseError: typeof Errors.BrowserbaseError;
    static APIError: typeof Errors.APIError;
    static APIConnectionError: typeof Errors.APIConnectionError;
    static APIConnectionTimeoutError: typeof Errors.APIConnectionTimeoutError;
    static APIUserAbortError: typeof Errors.APIUserAbortError;
    static NotFoundError: typeof Errors.NotFoundError;
    static ConflictError: typeof Errors.ConflictError;
    static RateLimitError: typeof Errors.RateLimitError;
    static BadRequestError: typeof Errors.BadRequestError;
    static AuthenticationError: typeof Errors.AuthenticationError;
    static InternalServerError: typeof Errors.InternalServerError;
    static PermissionDeniedError: typeof Errors.PermissionDeniedError;
    static UnprocessableEntityError: typeof Errors.UnprocessableEntityError;
    static toFile: typeof Uploads.toFile;
    static fileFromPath: typeof Uploads.fileFromPath;
}
export declare const BrowserbaseError: typeof Errors.BrowserbaseError, APIError: typeof Errors.APIError, APIConnectionError: typeof Errors.APIConnectionError, APIConnectionTimeoutError: typeof Errors.APIConnectionTimeoutError, APIUserAbortError: typeof Errors.APIUserAbortError, NotFoundError: typeof Errors.NotFoundError, ConflictError: typeof Errors.ConflictError, RateLimitError: typeof Errors.RateLimitError, BadRequestError: typeof Errors.BadRequestError, AuthenticationError: typeof Errors.AuthenticationError, InternalServerError: typeof Errors.InternalServerError, PermissionDeniedError: typeof Errors.PermissionDeniedError, UnprocessableEntityError: typeof Errors.UnprocessableEntityError;
export import toFile = Uploads.toFile;
export import fileFromPath = Uploads.fileFromPath;
export declare namespace Browserbase {
    export import RequestOptions = Core.RequestOptions;
    export import Contexts = API.Contexts;
    export import Context = API.Context;
    export import ContextCreateResponse = API.ContextCreateResponse;
    export import ContextUpdateResponse = API.ContextUpdateResponse;
    export import ContextCreateParams = API.ContextCreateParams;
    export import Extensions = API.Extensions;
    export import Extension = API.Extension;
    export import ExtensionCreateParams = API.ExtensionCreateParams;
    export import Projects = API.Projects;
    export import Project = API.Project;
    export import ProjectUsage = API.ProjectUsage;
    export import ProjectListResponse = API.ProjectListResponse;
    export import Sessions = API.Sessions;
    export import Session = API.Session;
    export import SessionLiveURLs = API.SessionLiveURLs;
    export import SessionCreateResponse = API.SessionCreateResponse;
    export import SessionListResponse = API.SessionListResponse;
    export import SessionCreateParams = API.SessionCreateParams;
    export import SessionUpdateParams = API.SessionUpdateParams;
    export import SessionListParams = API.SessionListParams;
}
export default Browserbase;
//# sourceMappingURL=index.d.ts.map