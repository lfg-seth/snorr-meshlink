// Local development opens the database demo; production defaults to sign-in.
export function portalBuildMode(development: boolean, requested?: string): 'live' | 'demo' {
  if (requested !== undefined && requested !== 'live' && requested !== 'demo')
    throw new Error('VITE_PORTAL_MODE must be live or demo.');
  return requested ?? (development ? 'demo' : 'live');
}
