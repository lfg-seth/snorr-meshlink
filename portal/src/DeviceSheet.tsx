import { lazy, Suspense, useEffect, useRef } from 'react';
import type { ReactNode } from 'react';
import type { MiniMapNode } from './CardMiniMap';

const CardMiniMap = lazy(() => import('./CardMiniMap'));

// Native dialogs provide focus containment, Escape and an inert background on mobile.
// Desktop uses the same content as a nonmodal panel above the map.
export default function DeviceSheet({ label, eyebrow, status, className, closeLabel, onClose, children, mapNodes, mapColor }: {
  label: string;
  eyebrow: string;
  status?: ReactNode;
  className: string;
  closeLabel: string;
  onClose: () => void;
  children: ReactNode;
  mapNodes?: MiniMapNode[];
  mapColor?: string;
}) {
  const dialog = useRef<HTMLDialogElement>(null);
  const gestureStart = useRef<number | null>(null);
  useEffect(() => {
    const element = dialog.current!;
    const previousFocus = document.activeElement;
    const mobile = window.matchMedia('(max-width: 850px)');
    const display = () => {
      if (element.open) element.close();
      if (mobile.matches) element.showModal();
      else element.show();
    };
    display();
    mobile.addEventListener('change', display);
    return () => {
      mobile.removeEventListener('change', display);
      element.close();
      if (previousFocus instanceof HTMLElement && previousFocus.isConnected) previousFocus.focus();
    };
  }, []);
  return (
    <dialog ref={dialog} className={`device-sheet ${className}`} aria-label={label}
      onCancel={(event) => { event.preventDefault(); onClose(); }}
      onKeyDown={(event) => {
        // Nonmodal desktop dialogs do not receive native cancel events.
        if (event.key === 'Escape') { event.preventDefault(); onClose(); }
      }}
      onClick={(event) => {
        if (event.target !== event.currentTarget) return;
        const bounds = event.currentTarget.getBoundingClientRect();
        if (event.clientX < bounds.left || event.clientX > bounds.right ||
            event.clientY < bounds.top || event.clientY > bounds.bottom) onClose();
      }}>
      <div className="device-sheet-header">
        <div className="sheet-drag-area" aria-hidden="true"
          onPointerDown={(event) => {
            gestureStart.current = event.clientY;
            event.currentTarget.setPointerCapture(event.pointerId);
          }}
          onPointerUp={(event) => {
            if (gestureStart.current !== null && event.clientY - gestureStart.current > 80) onClose();
            gestureStart.current = null;
          }}
          onPointerCancel={() => { gestureStart.current = null; }}>
          <span className="sheet-handle" />
        </div>
        <div className="panel-heading">
          <div><p className="eyebrow">{eyebrow}</p><div className="sheet-title"><h2>{label}</h2>{status}</div></div>
          <button autoFocus aria-label={closeLabel} onClick={onClose}>Close</button>
        </div>
      </div>
      <div className="device-sheet-content">
        {mapNodes && <Suspense fallback={<div className="mini-map-loading">Loading map…</div>}>
          <CardMiniMap nodes={mapNodes} color={mapColor} />
        </Suspense>}
        {children}
      </div>
    </dialog>
  );
}
