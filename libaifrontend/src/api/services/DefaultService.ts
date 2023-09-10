/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_token_from_login_user_tokenlogin_post } from '../models/Body_token_from_login_user_tokenlogin_post';
import type { Token } from '../models/Token';
import type { UserCreate } from '../models/UserCreate';
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
    public static registerUserUserCreatePost(
        requestBody: UserCreate,
    ): CancelablePromise<UserOutToken> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/user/create',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Token From Login
     * @param formData
     * @returns Token Successful Response
     * @throws ApiError
     */
    public static tokenFromLoginUserTokenloginPost(
        formData: Body_token_from_login_user_tokenlogin_post,
    ): CancelablePromise<Token> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/user/tokenlogin',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
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
            url: '/user/me',
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
