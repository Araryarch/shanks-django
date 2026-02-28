"""
Complete Authentication Routes with Email Verification
"""
from shanks import App
from internal.controller import auth_controller

router = App()

# Group all auth routes under /api/auth
with router.group('/api/auth'):
    
    @router.post('/register')
    def register_route(req):
        """Register new user"""
        return auth_controller.register(req)

    @router.post('/verify-email')
    def verify_email_route(req):
        """Verify email with code"""
        return auth_controller.verify_email(req)

    @router.post('/resend-verification')
    def resend_verification_route(req):
        """Resend verification email"""
        return auth_controller.resend_verification(req)

    @router.post('/login')
    def login_route(req):
        """Login user"""
        return auth_controller.login_user(req)

    @router.post('/forgot-password')
    def forgot_password_route(req):
        """Request password reset"""
        return auth_controller.forgot_password(req)

    @router.post('/reset-password')
    def reset_password_route(req):
        """Reset password with code"""
        return auth_controller.reset_password(req)

    @router.post('/logout')
    def logout_route(req):
        """Logout user"""
        return auth_controller.logout_user(req)

    @router.get('/me')
    def me_route(req):
        """Get current user info"""
        return auth_controller.get_current_user(req)
