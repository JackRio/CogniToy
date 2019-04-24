const { body } = document;
const fullWidth = body.clientWidth;
const fullHeight = body.clientHeight;

const mouse$ = Rx.Observable
  .fromEvent(body, 'mousemove')
  .map(({ offsetX, offsetY }) => ({
    x: offsetX / fullWidth,
    y: offsetY / fullHeight
  }));

mouse$.subscribe(({ x, y }) => {
  body.style.setProperty('--mouse-x', x);
  body.style.setProperty('--mouse-y', y);
});