import { createContext, useContext, useState } from 'react';
import type { ReactNode, Dispatch, SetStateAction } from 'react';
import type { Basemap } from './map-style';

const BasemapContext = createContext<[Basemap, Dispatch<SetStateAction<Basemap>>] | null>(null);

export function MapPreferences({ children }: { children: ReactNode }) {
  const selection = useState<Basemap>('Topo');
  return <BasemapContext.Provider value={selection}>{children}</BasemapContext.Provider>;
}

export function useBasemap() {
  const local = useState<Basemap>('Topo');
  return useContext(BasemapContext) ?? local;
}
