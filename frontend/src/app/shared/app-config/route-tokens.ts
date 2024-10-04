export const ROUTE_TOKENS = {
  LOGIN: 'login',
  PROFILE: 'profile',
  REGISTRATION: {
    REGISTRATION: 'registration',
    CONFIRMATION_CODE: 'registration-code',
    CREATE_PASSWORD: 'registration-new-password',
    REGISTRATION_SUCCESS: 'registration-success',
  },
  RESET_PASSWORD: {
    RESET_PASSWORD: 'reset-password',
    CONFIRMATION_CODE: 'reset-password-code',
    CREATE_PASSWORD: 'reset-password-new-password',
    RESET_PASSWORD_SUCCESS: 'reset-password-success',
  },
  MAIN: 'main',

} as const;
