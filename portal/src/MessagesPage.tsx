import Badge from './Badge';
import { timeLabel } from './demo';
import type { Message } from './demo';
export default function MessagesPage({
  messages,
  draft,
  onDraft,
  online,
  admin,
  onSend,
  onIncoming,
}: {
  messages: Message[];
  draft: string;
  onDraft: (text: string) => void;
  online: boolean;
  admin: boolean;
  onSend: () => void;
  onIncoming: () => void;
}) {
  return (
    <div className="messages-layout">
      <section className="panel message-panel">
        <div className="panel-heading">
          <div>
            <h2>Shared operational channel</h2>
            <span className="muted small">
              Chronological · fictional training traffic
            </span>
          </div>
          <button disabled={!online} onClick={onIncoming}>
            Simulate inbound
          </button>
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
          onSubmit={(event) => {
            event.preventDefault();
            onSend();
          }}
        >
          <label htmlFor="message-draft">
            Message as {admin ? 'Demo Dispatch' : 'Demo Casey'}
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
              {online
                ? 'Manual send · author prefix added'
                : 'Draft preserved · reconnect, then send manually'}
            </span>
            <button
              className="primary"
              disabled={!online || !draft.trim()}
              type="submit"
            >
              Simulate send
            </button>
          </div>
        </form>
      </section>
      <aside className="panel message-notes">
        <p className="eyebrow">Send evidence</p>
        <h2>Know what was received</h2>
        <p>
          A simulated gateway submission does not prove radio delivery or human
          receipt.
        </p>
        <p>
          Only the designated demo dispatch gateway represents a downlink path.
          The second gateway is uplink-only.
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
