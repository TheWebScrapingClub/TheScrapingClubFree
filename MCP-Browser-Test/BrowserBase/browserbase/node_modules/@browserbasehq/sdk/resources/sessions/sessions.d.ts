import { APIResource } from "../../resource.js";
import * as Core from "../../core.js";
import * as SessionsAPI from "./sessions.js";
import * as DownloadsAPI from "./downloads.js";
import * as LogsAPI from "./logs.js";
import * as RecordingAPI from "./recording.js";
import * as UploadsAPI from "./uploads.js";
export declare class Sessions extends APIResource {
    downloads: DownloadsAPI.Downloads;
    logs: LogsAPI.Logs;
    recording: RecordingAPI.Recording;
    uploads: UploadsAPI.Uploads;
    /**
     * Create a Session
     */
    create(body: SessionCreateParams, options?: Core.RequestOptions): Core.APIPromise<SessionCreateResponse>;
    /**
     * Session
     */
    retrieve(id: string, options?: Core.RequestOptions): Core.APIPromise<Session>;
    /**
     * Update Session
     */
    update(id: string, body: SessionUpdateParams, options?: Core.RequestOptions): Core.APIPromise<Session>;
    /**
     * List Sessions
     */
    list(query?: SessionListParams, options?: Core.RequestOptions): Core.APIPromise<SessionListResponse>;
    list(options?: Core.RequestOptions): Core.APIPromise<SessionListResponse>;
    /**
     * Session Live URLs
     */
    debug(id: string, options?: Core.RequestOptions): Core.APIPromise<SessionLiveURLs>;
}
export interface Session {
    id: string;
    createdAt: string;
    expiresAt: string;
    /**
     * Indicates if the Session was created to be kept alive upon disconnections
     */
    keepAlive: boolean;
    /**
     * The Project ID linked to the Session.
     */
    projectId: string;
    /**
     * Bytes used via the [Proxy](/features/stealth-mode#proxies-and-residential-ips)
     */
    proxyBytes: number;
    /**
     * The region where the Session is running.
     */
    region: 'us-west-2' | 'us-east-1' | 'eu-central-1' | 'ap-southeast-1';
    startedAt: string;
    status: 'RUNNING' | 'ERROR' | 'TIMED_OUT' | 'COMPLETED';
    updatedAt: string;
    /**
     * CPU used by the Session
     */
    avgCpuUsage?: number;
    /**
     * Optional. The Context linked to the Session.
     */
    contextId?: string;
    endedAt?: string;
    /**
     * Memory used by the Session
     */
    memoryUsage?: number;
}
export interface SessionLiveURLs {
    debuggerFullscreenUrl: string;
    debuggerUrl: string;
    pages: Array<SessionLiveURLs.Page>;
    wsUrl: string;
}
export declare namespace SessionLiveURLs {
    interface Page {
        id: string;
        debuggerFullscreenUrl: string;
        debuggerUrl: string;
        faviconUrl: string;
        title: string;
        url: string;
    }
}
export interface SessionCreateResponse {
    id: string;
    /**
     * WebSocket URL to connect to the Session.
     */
    connectUrl: string;
    createdAt: string;
    expiresAt: string;
    /**
     * Indicates if the Session was created to be kept alive upon disconnections
     */
    keepAlive: boolean;
    /**
     * The Project ID linked to the Session.
     */
    projectId: string;
    /**
     * Bytes used via the [Proxy](/features/stealth-mode#proxies-and-residential-ips)
     */
    proxyBytes: number;
    /**
     * The region where the Session is running.
     */
    region: 'us-west-2' | 'us-east-1' | 'eu-central-1' | 'ap-southeast-1';
    /**
     * HTTP URL to connect to the Session.
     */
    seleniumRemoteUrl: string;
    /**
     * Signing key to use when connecting to the Session via HTTP.
     */
    signingKey: string;
    startedAt: string;
    status: 'RUNNING' | 'ERROR' | 'TIMED_OUT' | 'COMPLETED';
    updatedAt: string;
    /**
     * CPU used by the Session
     */
    avgCpuUsage?: number;
    /**
     * Optional. The Context linked to the Session.
     */
    contextId?: string;
    endedAt?: string;
    /**
     * Memory used by the Session
     */
    memoryUsage?: number;
}
export type SessionListResponse = Array<Session>;
export interface SessionCreateParams {
    /**
     * The Project ID. Can be found in
     * [Settings](https://www.browserbase.com/settings).
     */
    projectId: string;
    browserSettings?: SessionCreateParams.BrowserSettings;
    /**
     * The uploaded Extension ID. See
     * [Upload Extension](/reference/api/upload-an-extension).
     */
    extensionId?: string;
    /**
     * Set to true to keep the session alive even after disconnections. This is
     * available on the Startup plan only.
     */
    keepAlive?: boolean;
    /**
     * Proxy configuration. Can be true for default proxy, or an array of proxy
     * configurations.
     */
    proxies?: boolean | Array<SessionCreateParams.BrowserbaseProxyConfig | SessionCreateParams.ExternalProxyConfig>;
    /**
     * The region where the Session should run.
     */
    region?: 'us-west-2' | 'us-east-1' | 'eu-central-1' | 'ap-southeast-1';
    /**
     * Duration in seconds after which the session will automatically end. Defaults to
     * the Project's `defaultTimeout`.
     */
    timeout?: number;
}
export declare namespace SessionCreateParams {
    interface BrowserSettings {
        /**
         * Enable or disable ad blocking in the browser. Defaults to `false`.
         */
        blockAds?: boolean;
        context?: BrowserSettings.Context;
        /**
         * The uploaded Extension ID. See
         * [Upload Extension](/reference/api/upload-an-extension).
         */
        extensionId?: string;
        /**
         * See usage examples
         * [in the Stealth Mode page](/features/stealth-mode#fingerprinting).
         */
        fingerprint?: BrowserSettings.Fingerprint;
        /**
         * Enable or disable session logging. Defaults to `true`.
         */
        logSession?: boolean;
        /**
         * Enable or disable session recording. Defaults to `true`.
         */
        recordSession?: boolean;
        /**
         * Enable or disable captcha solving in the browser. Defaults to `true`.
         */
        solveCaptchas?: boolean;
        viewport?: BrowserSettings.Viewport;
    }
    namespace BrowserSettings {
        interface Context {
            /**
             * The Context ID.
             */
            id: string;
            /**
             * Whether or not to persist the context after browsing. Defaults to `false`.
             */
            persist?: boolean;
        }
        /**
         * See usage examples
         * [in the Stealth Mode page](/features/stealth-mode#fingerprinting).
         */
        interface Fingerprint {
            browsers?: Array<'chrome' | 'edge' | 'firefox' | 'safari'>;
            devices?: Array<'desktop' | 'mobile'>;
            httpVersion?: 1 | 2;
            /**
             * Full list of locales is available
             * [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept-Language).
             */
            locales?: Array<string>;
            /**
             * Note: `operatingSystems` set to `ios` or `android` requires `devices` to include
             * `"mobile"`.
             */
            operatingSystems?: Array<'android' | 'ios' | 'linux' | 'macos' | 'windows'>;
            screen?: Fingerprint.Screen;
        }
        namespace Fingerprint {
            interface Screen {
                maxHeight?: number;
                maxWidth?: number;
                minHeight?: number;
                minWidth?: number;
            }
        }
        interface Viewport {
            height?: number;
            width?: number;
        }
    }
    interface BrowserbaseProxyConfig {
        /**
         * Type of proxy. Always use 'browserbase' for the Browserbase managed proxy
         * network.
         */
        type: 'browserbase';
        /**
         * Domain pattern for which this proxy should be used. If omitted, defaults to all
         * domains. Optional.
         */
        domainPattern?: string;
        /**
         * Configuration for geolocation
         */
        geolocation?: BrowserbaseProxyConfig.Geolocation;
    }
    namespace BrowserbaseProxyConfig {
        /**
         * Configuration for geolocation
         */
        interface Geolocation {
            /**
             * Country code in ISO 3166-1 alpha-2 format
             */
            country: string;
            /**
             * Name of the city. Use spaces for multi-word city names. Optional.
             */
            city?: string;
            /**
             * US state code (2 characters). Must also specify US as the country. Optional.
             */
            state?: string;
        }
    }
    interface ExternalProxyConfig {
        /**
         * Server URL for external proxy. Required.
         */
        server: string;
        /**
         * Type of proxy. Always 'external' for this config.
         */
        type: 'external';
        /**
         * Domain pattern for which this proxy should be used. If omitted, defaults to all
         * domains. Optional.
         */
        domainPattern?: string;
        /**
         * Password for external proxy authentication. Optional.
         */
        password?: string;
        /**
         * Username for external proxy authentication. Optional.
         */
        username?: string;
    }
}
export interface SessionUpdateParams {
    /**
     * The Project ID. Can be found in
     * [Settings](https://www.browserbase.com/settings).
     */
    projectId: string;
    /**
     * Set to `REQUEST_RELEASE` to request that the session complete. Use before
     * session's timeout to avoid additional charges.
     */
    status: 'REQUEST_RELEASE';
}
export interface SessionListParams {
    status?: 'RUNNING' | 'ERROR' | 'TIMED_OUT' | 'COMPLETED';
}
export declare namespace Sessions {
    export import Session = SessionsAPI.Session;
    export import SessionLiveURLs = SessionsAPI.SessionLiveURLs;
    export import SessionCreateResponse = SessionsAPI.SessionCreateResponse;
    export import SessionListResponse = SessionsAPI.SessionListResponse;
    export import SessionCreateParams = SessionsAPI.SessionCreateParams;
    export import SessionUpdateParams = SessionsAPI.SessionUpdateParams;
    export import SessionListParams = SessionsAPI.SessionListParams;
    export import Downloads = DownloadsAPI.Downloads;
    export import Logs = LogsAPI.Logs;
    export import SessionLog = LogsAPI.SessionLog;
    export import LogListResponse = LogsAPI.LogListResponse;
    export import Recording = RecordingAPI.Recording;
    export import SessionRecording = RecordingAPI.SessionRecording;
    export import RecordingRetrieveResponse = RecordingAPI.RecordingRetrieveResponse;
    export import Uploads = UploadsAPI.Uploads;
    export import UploadCreateResponse = UploadsAPI.UploadCreateResponse;
    export import UploadCreateParams = UploadsAPI.UploadCreateParams;
}
//# sourceMappingURL=sessions.d.ts.map