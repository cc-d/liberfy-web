/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Token } from '../models/Token';
import type { UserNew } from '../models/UserNew';
import type { UserOut } from '../models/UserOut';
import type { UserOutToken } from '../models/UserOutToken';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Register User
     * @param requestBody
     * @returns UserOutToken Successful Response
     * @throws ApiError
     */
    public static registerUserUserNewPost(
        requestBody: UserNew,
    ): CancelablePromise<UserOutToken> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/u/create',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Token From Login
     * @returns Token Successful Response
     * @throws ApiError
     */
    public static tokenFromLoginUserTokenloginPost(): CancelablePromise<Token> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/u/tokenlogin',
        });
    }

    /**
     * Read Users Me
     * @returns UserOut Successful Response
     * @throws ApiError
     */
    public static readUsersMeUserMeGet(): CancelablePromise<UserOut> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/u/me',
        });
    }

    /**
     * Hello
     * @returns any Successful Response
     * @throws ApiError
     */
    public static helloGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/',
        });
    }

    /**
     * Get Openapi Schema
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getOpenapiSchemaOpenapiJsonGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/openapi.json',
        });
    }

}
