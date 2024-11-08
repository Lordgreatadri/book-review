from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import FastAPI, status
from typing import Any, Callable




class BaseExceptionClass(Exception):
    """The base class for exception handling"""
    pass


class InvalidToken(BaseExceptionClass):
    """Invalid or expired token provided."""
    pass
    # HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN, 
    #             detail={
    #                 "status_code":status.HTTP_403_FORBIDDEN,
    #                 "error":"Token is invalid or expired",
    #                 "resolution":"Please create a new token"
    #             }
    #         )

class RevokedToken(BaseExceptionClass):
    """Revoked token provided."""
    pass
    # HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN, 
    #             detail={
    #                 "status_code":status.HTTP_403_FORBIDDEN,
    #                 "error":"Token is either revoked or invalid",
    #                 "resolution":"Please create a new token"
    #                 }
    #             )




class AccessTokenRequired(BaseExceptionClass):
    """Refresh token was provided instead of access token."""
    pass    
    # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN, 
            #     detail={
            #         "status_code":status.HTTP_403_FORBIDDEN,
            #         "error":"Please provide a valid access_token"
            #         }
            # )


class RefreshTokenRequired(BaseExceptionClass):
    """Access token was provided instead of refresh token."""
    pass    
    #HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN, 
        #         detail={
        #             "status_code":status.HTTP_403_FORBIDDEN,
        #             "error":"Please provide a valid refresh_token"
        #             }
        #     )


class UserAlreadyExists(BaseExceptionClass):
    """User record is already exists"""
    pass 
#HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")



class UserEmailAlreadyExists(BaseExceptionClass):
    """User has provided an existing email address at sign up."""
    pass 
    #HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already registered")
       




class UserPhoneNumberAlreadyExists(BaseExceptionClass):
    """User has provided an existing phone number at sign up."""
    pass 
    #HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Phone number already registered")
    




class UsernameAlreadyExists(BaseExceptionClass):
    """User has provided an existing username at sign up."""
    pass
    #HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username already registered")




class InsufficientPermission(BaseExceptionClass):
    """User does not have sufficient permissions to perform the requested action."""
    pass
# HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail={
#                 "status_code": status.HTTP_403_FORBIDDEN,
#                 "error":"Access denied",
#                 "message":"You are not permitted to perform this action."
#             }
#         )




class SpecifiedResourceNotFound(BaseExceptionClass):
    """Specified resource not found."""
    pass



class BookNotFound(BaseExceptionClass):
    """Book not found."""
    pass
#HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The specified book with {book_uid} not found.")




class TagNotFound(BaseExceptionClass):
    """Tag not found."""
    pass 


class TagAlreadyExists(BaseExceptionClass):
    """Tag already exists."""
    pass


class UserNotFound(BaseExceptionClass):
    """User not found."""
    pass


class InvalidUserCredentials(BaseExceptionClass):
    """Invalid user credentials provided at log in."""
    pass
    #HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

class NotFound(BaseExceptionClass):
    """Resource not found."""
    pass


class InvalidBookData(BaseExceptionClass):
    """Invalid book data provided."""
    pass



class InvalidReviewData(BaseExceptionClass):
    """Invalid review data provided."""
    pass



class NewResourceServerError(BaseExceptionClass):
    """Internal server error occurred while creating a new resource."""
    pass
    # HTTPException(status_code=500, detail={
    #     "status_code": status.HTTP_500,
    #     "error":"An error occurred while creating new resource"
    #     }
    #     )






def create_exception_handler(status_code: int, detail:Any)->Callable[[Request, Exception], JSONResponse]:
    """Create a custom exception handler."""
    async def exception_handler(request: Request, exc:BaseExceptionClass):
        return JSONResponse(
            status_code = status_code,
            content = detail,
            # headers = {"Content-Type": "application/json"}
        )
    
        # return JSONResponse(
        #     status_code=status_code,
        #     content={
        #         "status_code": status_code,
        #         "error": exc.__class__.__name__,
        #         "detail": details if details else exc.args[0]
        #     }
        # )

    return exception_handler




def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status_code": status.HTTP_409_CONFLICT,
                "message": "User already exists",
                "error_code": "USER_EXISTS"
            }
        )
    )


    app.add_exception_handler(
        UserEmailAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status_code": status.HTTP_409_CONFLICT,
                "message": "User email already taken",
                "error_code": "USER_EMAIL_TAKEN"
            }
        )
    )

    app.add_exception_handler(
        UserPhoneNumberAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status_code": status.HTTP_409_CONFLICT,
                "message": "User phone number already taken",
                "error_code": "USER_PHONE_NUMBER_TAKEN"
            }
        )
    )

    app.add_exception_handler(
        UsernameAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status_code": status.HTTP_409_CONFLICT,
                "message": "Username already taken",
                "error_code": "USER_NAME_TAKEN"
            }
        )
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "message": "User not found",
                "error_code": "USER_NOT_FOUND",
            },
        ),
    )

    app.add_exception_handler(
        InvalidUserCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid Email Or Password",
                "error_code": "INVALID_EMAIL_OR_PASSWORD",
            }
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Token is invalid Or expired",
                "resolution": "Please create a new token",
                "error_code": "INVALID_TOKEN",
            },
        ),
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Token is invalid or has been revoked",
                "resolution": "Please create a new token",
                "error_code": "TOKEN_REVOKED",
            },
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status": status.HTTP_403_FORBIDDEN,
                "message": "Please provide a valid access token",
                "resolution": "Please provide an access token",
                "error_code": "ACCESS_TOKEN_REQUIRED",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status": status.HTTP_403_FORBIDDEN,
                "message": "Please provide a valid refresh token",
                "resolution": "Please provide an refresh token",
                "error_code": "REFRESH_TOKEN_REQUIRED",
            },
        ),
    )

    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status" : status.HTTP_401_UNAUTHORIZED,
                "message": "You do not have enough permissions to perform this action",
                "error_code": "INSUFFICIENT_PERMISSIONS",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Specified book not found",
                "error_code": "BOOK_NOT_FOUND",
            },
        ),
    )

    app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Tag Not Found", 
                "error_code": "TAG_NOT_FOUND",
            },
        ),
    )

    app.add_exception_handler(
        TagAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status": status.HTTP_409_CONFLICT,
                "message": "Tag already exists",
                "error_code": "TAG_EXISTS",
            },
        ),
    )



    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Sorry! Something went wrong",
                "error_code": "INTERNAL_SERVER_ERROR",
            },
            
        )


    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )