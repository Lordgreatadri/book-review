


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



class NewResourceServerError(BaseException):
    """Internal server error occurred while creating a new resource."""
    pass
    # HTTPException(status_code=500, detail={
    #     "status_code": status.HTTP_500,
    #     "error":"An error occurred while creating new resource"
    #     }
    #     )








