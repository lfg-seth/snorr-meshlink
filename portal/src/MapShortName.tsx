import { useState } from 'react';

export default function MapShortName({ shortName, onSave }: {
  shortName: string;
  onSave: (shortName: string) => Promise<boolean>;
}) {
  const [draft, setDraft] = useState(shortName);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  return (
    <section className="panel">
      <h2>Your map shortname</h2>
      <p className="small muted">Choose up to 5 letters, numbers, underscores or dashes for your assigned tracker’s map icon.</p>
      <form className="map-shortname-form" onSubmit={async (event) => {
        event.preventDefault();
        setSaving(true);
        setMessage('');
        try {
          setMessage(await onSave(draft.trim()) ? 'Map shortname saved.' : 'Could not save map shortname.');
        } catch {
          setMessage('Could not save map shortname.');
        } finally {
          setSaving(false);
        }
      }}>
        <label>Shortname <input name="shortName" required minLength={1} maxLength={5}
          pattern="[A-Za-z0-9_\-]{1,5}" value={draft} autoComplete="off"
          onChange={(event) => setDraft(event.target.value)} disabled={saving} /></label>
        <button type="submit" disabled={saving}>{saving ? 'Saving…' : 'Save shortname'}</button>
      </form>
      <p className="small" role="status">{message}</p>
    </section>
  );
}
