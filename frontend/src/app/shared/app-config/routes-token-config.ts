export const ROUTES_TOKEN_CONFIG = {
  LOGIN: 'login',
  MAIN: 'main',
  CATEGORIES: 'categories',
  SEARCH: 'search',
  FAVOURITES: 'favourites',
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
} as const;
