// DOM marker adapter for interaction tests; does not simulate WebGL or map tiles.
export function setWorkerUrl() {}
export class Map {
  constructor({ container }) {
    this.container = container;
  }
  addControl() {}
  on() {}
  resize() {}
  remove() {}
  getSource(name) {
    return { setData: (data) => { this.container.dataset[name] = JSON.stringify(data); } };
  }
  easeTo() {}
  fitBounds() {}
}
export class Marker {
  constructor({ element }) {
    this.element = element;
  }
  setLngLat() {
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
