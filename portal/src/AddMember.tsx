import { useRef, useState } from 'react';

export type NewMember = { name: string; username: string; password: string; shortName?: string };

export default function AddMember({ onCreate, onCreated, disabled = false }: {
  onCreate: (member: NewMember) => Promise<string>;
  onCreated: (id: string) => void;
  disabled?: boolean;
}) {
  const [pending, setPending] = useState(false);
  const submitting = useRef(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  return <section className="panel">
    <h2>Add member</h2>
    <p className="muted small">Create a member and their sign-in, then assign them a tracker below.</p>
    <form className="assignment-form" onSubmit={async event => {
      event.preventDefault();
      if (submitting.current || disabled) return;
      const form = event.currentTarget;
      const fields = new FormData(form);
      const name = String(fields.get('name')).trim();
      const shortName = String(fields.get('shortName')).trim();
      submitting.current = true;
      setPending(true);
      setError('');
      setSuccess('');
      try {
        const id = await onCreate({ name, username: String(fields.get('username')).trim(),
          password: String(fields.get('password')), ...(shortName ? { shortName } : {}) });
        form.reset();
        onCreated(id);
        setSuccess(`${name} added. Select a tracker below to assign it.`);
      } catch (error) {
        setError(error instanceof Error ? error.message : 'Unable to add member.');
      } finally {
        submitting.current = false;
        setPending(false);
      }
    }}>
      <fieldset disabled={pending || disabled} className="add-member-fields">
        <label>Full name<input name="name" required maxLength={80} autoComplete="off" /></label>
        <label>Username<input name="username" required maxLength={80} pattern="[a-zA-Z0-9_.\-]+" autoComplete="off" /></label>
        <label>Initial password<input name="password" type="password" required minLength={12} maxLength={200} autoComplete="new-password" /></label>
        <label>Map shortname (optional)<input name="shortName" maxLength={5} pattern="[a-zA-Z0-9_\-]{1,5}" autoComplete="off" /></label>
        <button className="primary" type="submit">{pending ? 'Adding member…' : 'Add member'}</button>
      </fieldset>
    </form>
    {error && <p className="form-error" role="alert">{error}</p>}
    {success && <p role="status">{success}</p>}
  </section>;
}
