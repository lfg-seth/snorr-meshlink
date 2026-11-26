import { useRef, useState } from 'react';
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
  simulation,
  receiverOnline,
  feedback,
}: {
  messages: Message[];
  authorName?: string;
  draft: string;
  onDraft: (text: string) => void;
  online: boolean;
  admin: boolean;
  onSend: () => void | Promise<void>;
  onIncoming?: () => void;
  simulation: boolean;
  receiverOnline: boolean;
  feedback: string;
}) {
  const [sending, setSending] = useState(false);
  const busy = useRef(false);
  const bytes = new TextEncoder().encode(`${authorName}: ${draft.trim()}`).length;
  const oversized = !simulation && bytes > 233;
  return (
    <div className="messages-layout">
      <section className="panel message-panel">
        <div className="panel-heading">
          <div>
            <h2>Shared operational channel</h2>
            <span className="muted small">
              {simulation ? 'Chronological · fictional training traffic'
                : `SNORRbench · ${receiverOnline ? 'receiver connected' : 'receiver offline'}`}
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
            if (busy.current || oversized || !online || !draft.trim()) return;
            busy.current = true;
            setSending(true);
            try {
              await onSend();
            } finally {
              busy.current = false;
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
              {online
                ? 'Manual send · author prefix added'
                : 'Draft preserved · reconnect, then send manually'}
              {!simulation && ` · ${bytes}/233 bytes with author`}
            </span>
            <button
              className="primary"
              disabled={sending || oversized || !online || !draft.trim()}
              type="submit"
            >
              {sending ? 'Sending…' : simulation ? 'Simulate send' : online ? 'Send reply' : 'Send unavailable'}
            </button>
          </div>
          {feedback && <p role="status">{feedback}</p>}
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
          {simulation ? 'Messages in this demo stay in the training database.'
            : 'G008 at Seth’s Home relays dispatch replies onto SNORRbench.'}
        </p>
        <hr />
        <h3>During an outage</h3>
        <p>
          Your draft stays in this browser session. Restoring the feed never
          sends it automatically.
        </p>
      </aside>
    </div>
  );
}
