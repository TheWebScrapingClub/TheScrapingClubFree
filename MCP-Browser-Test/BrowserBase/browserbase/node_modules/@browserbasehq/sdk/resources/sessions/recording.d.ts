import { APIResource } from "../../resource.js";
import * as Core from "../../core.js";
import * as RecordingAPI from "./recording.js";
export declare class Recording extends APIResource {
    /**
     * Session Recording
     */
    retrieve(id: string, options?: Core.RequestOptions): Core.APIPromise<RecordingRetrieveResponse>;
}
export interface SessionRecording {
    id: string;
    /**
     * See
     * [rrweb documentation](https://github.com/rrweb-io/rrweb/blob/master/docs/recipes/dive-into-event.md).
     */
    data: Record<string, unknown>;
    sessionId: string;
    /**
     * milliseconds that have elapsed since the UNIX epoch
     */
    timestamp: number;
    type: number;
}
export type RecordingRetrieveResponse = Array<SessionRecording>;
export declare namespace Recording {
    export import SessionRecording = RecordingAPI.SessionRecording;
    export import RecordingRetrieveResponse = RecordingAPI.RecordingRetrieveResponse;
}
//# sourceMappingURL=recording.d.ts.map