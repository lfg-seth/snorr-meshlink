import { useState } from 'react';
import Badge from './Badge';
import { timeLabel } from './demo';
import type { Message } from './demo';
export default function MessagesPage({
  messages,
  authorName,
  draft,
  onDraft,
  online,
  admin,
  onSend,
  onIncoming,
  sendingEnabled = true,
}: {
  messages: Message[];
  authorName?: string;
  draft: string;
  onDraft: (text: string) => void;
  online: boolean;
  admin: boolean;
  onSend: () => void | Promise<void>;
  onIncoming?: () => void;
  sendingEnabled?: boolean;
}) {
  const [sending, setSending] = useState(false);
  return (
    <div className="messages-layout">
      <section className="panel message-panel">
        <div className="panel-heading">
          <div>
            <h2>Shared operational channel</h2>
            <span className="muted small">
              {sendingEnabled ? 'Chronological · fictional training traffic' : 'GPS integration only · messaging pending'}
            </span>
          </div>
          {onIncoming && (
            <button disabled={!online} onClick={onIncoming}>
              Simulate inbound
            </button>
          )}
        </div>
        <ol className="message-list">
          {messages.map((message) => (
            <li key={message.id}>
              <div className="message-meta">
                <strong>{message.author}</strong>
                <time dateTime={message.at}>{timeLabel(message.at)}</time>
              </div>
              <p>{message.text}</p>
              <span className="message-evidence">{message.evidence}</span>
            </li>
          ))}
        </ol>
        <form
          className="composer"
          onSubmit={async (event) => {
            event.preventDefault();
            if (sending || !sendingEnabled || !online || !draft.trim()) return;
            setSending(true);
            try {
              await onSend();
            } finally {
              setSending(false);
            }
          }}
        >
          <label htmlFor="message-draft">
            Message as {authorName ?? (admin ? 'Demo Dispatch' : 'Demo Casey')}
          </label>
          <textarea
            id="message-draft"
            rows={3}
            placeholder="Write a shared-channel reply…"
            value={draft}
            onChange={(event) => onDraft(event.target.value)}
          />
          <div>
            <span className="muted small">
              {!sendingEnabled ? 'Radio messaging is not integrated yet.' : online
                ? 'Manual send · author prefix added'
                : 'Draft preserved · reconnect, then send manually'}
            </span>
            <button
              className="primary"
              disabled={sending || !sendingEnabled || !online || !draft.trim()}
              type="submit"
            >
              {sending ? 'Sending…' : sendingEnabled ? 'Simulate send' : 'Send unavailable'}
            </button>
          </div>
        </form>
      </section>
      <aside className="panel message-notes">
        <p className="eyebrow">Send evidence</p>
        <h2>Know what was received</h2>
        <p>
          A gateway submission does not prove radio delivery or human
          receipt.
        </p>
        <p>
          Portal replies require a separately verified designated downlink gateway.
          The live GPS bench currently uses two uplink-only gateways.
        </p>
        <hr />
        <h3>During an outage</h3>
        <p>
          Your draft stays in this browser session. Restoring the feed never
          sends it automatically.
        </p>
        <p className="muted small">
          Live payload limits, expiry, authentication and delivery evidence
          await integration.
        </p>
      </aside>
    </div>
  );
}
