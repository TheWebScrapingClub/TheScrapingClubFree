import { APIResource } from "../resource.js";
import * as Core from "../core.js";
import * as ProjectsAPI from "./projects.js";
export declare class Projects extends APIResource {
    /**
     * Project
     */
    retrieve(id: string, options?: Core.RequestOptions): Core.APIPromise<Project>;
    /**
     * List all projects
     */
    list(options?: Core.RequestOptions): Core.APIPromise<ProjectListResponse>;
    /**
     * Project Usage
     */
    usage(id: string, options?: Core.RequestOptions): Core.APIPromise<ProjectUsage>;
}
export interface Project {
    id: string;
    createdAt: string;
    defaultTimeout: number;
    name: string;
    ownerId: string;
    updatedAt: string;
}
export interface ProjectUsage {
    browserMinutes: number;
    proxyBytes: number;
}
export type ProjectListResponse = Array<Project>;
export declare namespace Projects {
    export import Project = ProjectsAPI.Project;
    export import ProjectUsage = ProjectsAPI.ProjectUsage;
    export import ProjectListResponse = ProjectsAPI.ProjectListResponse;
}
//# sourceMappingURL=projects.d.ts.map