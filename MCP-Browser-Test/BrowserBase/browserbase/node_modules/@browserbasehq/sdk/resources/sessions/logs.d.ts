import { APIResource } from "../../resource.js";
import * as Core from "../../core.js";
import * as LogsAPI from "./logs.js";
export declare class Logs extends APIResource {
    /**
     * Session Logs
     */
    list(id: string, options?: Core.RequestOptions): Core.APIPromise<LogListResponse>;
}
export interface SessionLog {
    eventId: string;
    method: string;
    pageId: number;
    sessionId: string;
    /**
     * milliseconds that have elapsed since the UNIX epoch
     */
    timestamp: number;
    frameId?: string;
    loaderId?: string;
    request?: SessionLog.Request;
    response?: SessionLog.Response;
}
export declare namespace SessionLog {
    interface Request {
        params: Record<string, unknown>;
        rawBody: string;
        /**
         * milliseconds that have elapsed since the UNIX epoch
         */
        timestamp: number;
    }
    interface Response {
        rawBody: string;
        result: Record<string, unknown>;
        /**
         * milliseconds that have elapsed since the UNIX epoch
         */
        timestamp: number;
    }
}
export type LogListResponse = Array<SessionLog>;
export declare namespace Logs {
    export import SessionLog = LogsAPI.SessionLog;
    export import LogListResponse = LogsAPI.LogListResponse;
}
//# sourceMappingURL=logs.d.ts.map