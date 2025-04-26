import { APIResource } from "../../resource.js";
import * as Core from "../../core.js";
import * as UploadsAPI from "./uploads.js";
export declare class Uploads extends APIResource {
    /**
     * Create Session Uploads
     */
    create(id: string, body: UploadCreateParams, options?: Core.RequestOptions): Core.APIPromise<UploadCreateResponse>;
}
export interface UploadCreateResponse {
    message: string;
}
export interface UploadCreateParams {
    file: Core.Uploadable;
}
export declare namespace Uploads {
    export import UploadCreateResponse = UploadsAPI.UploadCreateResponse;
    export import UploadCreateParams = UploadsAPI.UploadCreateParams;
}
//# sourceMappingURL=uploads.d.ts.map