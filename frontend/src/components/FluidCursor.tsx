import { useEffect, useRef } from 'react';

export function FluidCursor() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rafRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current!;
    const ctx = canvas.getContext('2d')!;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const pointer = { x: width / 2, y: height / 2 };
    const trail: { x: number; y: number }[] = Array.from({ length: 18 }, () => ({ x: pointer.x, y: pointer.y }));

    const onMove = (e: PointerEvent) => {
      pointer.x = e.clientX;
      pointer.y = e.clientY;
    };
    const onResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('pointermove', onMove);
    window.addEventListener('resize', onResize);

    const render = () => {
      // follow pointer with easing
      for (let i = 0; i < trail.length; i++) {
        const target = i === 0 ? pointer : trail[i - 1];
        const p = trail[i];
        p.x += (target.x - p.x) * 0.2;
        p.y += (target.y - p.y) * 0.2;
      }

      ctx.clearRect(0, 0, width, height);
      for (let i = 0; i < trail.length - 1; i++) {
        const p1 = trail[i];
        const p2 = trail[i + 1];
        const alpha = 0.12 * (1 - i / trail.length);
        ctx.strokeStyle = `rgba(34,211,238,${alpha})`;
        ctx.lineWidth = Math.max(1, 10 - i * 0.5);
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();
      }

      rafRef.current = requestAnimationFrame(render);
    };
    rafRef.current = requestAnimationFrame(render);

    return () => {
      cancelAnimationFrame(rafRef.current!);
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('resize', onResize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="pointer-events-none fixed inset-0 z-10 mix-blend-screen"
    />
  );
}


