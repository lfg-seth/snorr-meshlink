export default function TrackerBatteryIcon({ battery }: { battery: number | null }) {
  const percent = battery !== null && Number.isFinite(battery) && battery >= 0 && battery <= 100
    ? Math.floor(battery) : null;
  const tone = percent === null ? 'unknown' : percent < 20 ? 'red' : percent < 40 ? 'amber' : 'green';
  const label = percent === null ? 'Battery unknown' : `Battery ${percent}%`;
  return (
    <svg className={`tracker-battery-icon ${tone}`} viewBox="0 0 30 14"
      role="img" aria-label={label}>
      <title>{label}</title>
      <rect x="1" y="1" width="25" height="12" rx="2" stroke="currentColor"
        strokeWidth="1.5" fill={percent === 100 ? 'currentColor' : 'none'} />
      <path d="M28.5 5v4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      {percent !== 100 && <text x="13.5" y="8" textAnchor="middle" dominantBaseline="middle"
        fontSize="9" fontWeight="700" fill="currentColor">
        {percent === null ? '—' : String(percent).padStart(2, '0')}
      </text>}
    </svg>
  );
}
