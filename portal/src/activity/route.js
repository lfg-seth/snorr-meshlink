export function receiptRoute(receipt) {
  const route = receipt.route;
  let label = "";
  if (route?.reception === "local") label = "Gateway";
  else if (route?.reception === "direct") label = "Direct";
  else if (Number.isInteger(route?.reportedHops) && route.reportedHops >= 0)
    label = route.reportedHops + (route.reportedHops === 1 ? " hop" : " hops");
  const relay = route?.reception === "relayed"
    ? route.lastRelayCandidate || route.lastRelayRadio || "" : "";
  const gateway = receipt.heardThrough || receipt.heardThroughRadio || "";
  return {label, relay, gateway};
}
