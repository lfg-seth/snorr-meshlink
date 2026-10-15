import { useState } from 'react';
import { login } from './backend';
import type { BackendSession } from './backend';
export default function BackendLogin({
  onLogin,
  onClose,
}: {
  onLogin: (session: BackendSession) => void;
  onClose?: () => void;
}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  return (
    <section className="panel backend-login" aria-label="Backend sign in">
      <div className="panel-heading">
        <h2>Sign in to MeshLink</h2>
        {onClose && <button onClick={onClose}>Close</button>}
      </div>
      <p className="small muted">
        Use the account created by the backend setup. The server enforces your
        role.
      </p>
      <form
        className="assignment-form"
        onSubmit={async (event) => {
          event.preventDefault();
          setBusy(true);
          setError('');
          try {
            onLogin(await login(username, password));
            setPassword('');
          } catch (e) {
            setError(e instanceof Error ? e.message : 'Sign in failed');
          } finally {
            setBusy(false);
          }
        }}
      >
        <label>
          Username
          <input
            autoComplete="username"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </label>
        <button className="primary" disabled={busy} type="submit">
          {busy ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
      {error && (
        <p role="alert" className="form-error">
          {error}
        </p>
      )}
    </section>
  );
}
