// Telemetry remains Celsius; convert only when presenting it to people.
export function temperatureLabel(celsius: number) {
  return `${((celsius * 9) / 5 + 32).toFixed(1)} °F`;
}
