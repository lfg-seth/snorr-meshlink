// DOM marker adapter for interaction tests; does not simulate WebGL or map tiles.
export function setWorkerUrl() {}
export class Map {
  constructor({ container, style, ...options }) {
    this.container = container;
    this.listeners = [];
    container.dataset.style = JSON.stringify(style);
    container.dataset.options = JSON.stringify(options);
    container.dataset.controls = '0';
  }
  addControl() { this.container.dataset.controls = String(Number(this.container.dataset.controls) + 1); }
  on(type, layer, listener) {
    if (typeof layer === 'function') {
      if (type === 'load') queueMicrotask(layer);
      return;
    }
    if (type === 'click') {
      const handler = event => {
        if (event.detail.layer === layer) listener({ features: [{ properties: { id: event.detail.id } }],
          originalEvent: { target: event.detail.target ?? this.container } });
      };
      this.container.addEventListener('test-map-click', handler);
      this.listeners.push(handler);
    }
  }
  resize() {}
  remove() { this.listeners.forEach(handler => this.container.removeEventListener('test-map-click', handler)); }
  getSource(name) {
    return { setData: (data) => { this.container.dataset[name] = JSON.stringify(data); } };
  }
  easeTo(options) { this.container.dataset.camera = JSON.stringify(options); }
  fitBounds(bounds, options) { this.container.dataset.camera = JSON.stringify({ bounds, ...options }); }
}
export class Marker {
  constructor({ element }) {
    this.element = element;
  }
  setLngLat(coordinates) {
    this.element.dataset.coordinates = JSON.stringify(coordinates);
    return this;
  }
  setOffset(offset) {
    this.element.dataset.offset = offset.join(',');
    return this;
  }
  addTo(map) {
    map.container.append(this.element);
    return this;
  }
  getElement() {
    return this.element;
  }
  remove() {
    this.element.remove();
  }
}
export class NavigationControl {}
export class AttributionControl {}
export class ScaleControl {}
