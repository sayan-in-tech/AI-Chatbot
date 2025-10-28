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
    let prevX = pointer.x;
    let prevY = pointer.y;

    type Particle = {
      x: number;
      y: number;
      vx: number;
      vy: number;
      life: number;
      maxLife: number;
      size: number;
      r: number;
      g: number;
      b: number;
    };
    const particles: Particle[] = [];

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
      // compute movement speed
      const dx = pointer.x - prevX;
      const dy = pointer.y - prevY;
      const speed = Math.sqrt(dx * dx + dy * dy);
      prevX = pointer.x;
      prevY = pointer.y;

      // emit particles proportional to speed
      const emit = Math.max(1, Math.min(6, Math.floor(speed / 8)));
      for (let i = 0; i < emit; i++) {
        // direction around movement with slight spread
        const angle = Math.atan2(dy, dx) + (Math.random() - 0.5) * 0.8;
        const power = 0.5 + Math.random() * 1.5 + speed * 0.02;
        const vx = Math.cos(angle) * power;
        const vy = Math.sin(angle) * power;
        const t = Math.random();
        const r = Math.round(251 * (1 - t) + 245 * t); // yellow->orange
        const g = Math.round(191 * (1 - t) + 158 * t);
        const b = Math.round(36 * (1 - t) + 11 * t);
        particles.push({
          x: pointer.x,
          y: pointer.y,
          vx,
          vy,
          life: 1,
          maxLife: 1 + Math.random() * 0.8,
          size: 2.5 + Math.random() * 2.5,
          r,
          g,
          b,
        });
      }

      // clear and draw
      ctx.clearRect(0, 0, width, height);
      ctx.globalCompositeOperation = 'lighter';

      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        // update
        p.x += p.vx;
        p.y += p.vy;
        p.vx *= 0.985; // friction
        p.vy = p.vy * 0.985 + 0.02; // slight gravity
        p.life -= 0.02;

        const alpha = Math.max(0, p.life / p.maxLife);
        const size = p.size * (0.5 + alpha * 0.5);

        // draw radial gradient spark
        ctx.shadowColor = `rgba(${p.r},${p.g},${p.b},${alpha * 0.6})`;
        ctx.shadowBlur = 12 * alpha;
        const grd = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, size);
        grd.addColorStop(0, `rgba(${p.r},${p.g},${p.b},${Math.min(0.9, 0.6 * alpha + 0.2)})`);
        grd.addColorStop(1, `rgba(${p.r},${p.g},${p.b},0)`);
        ctx.fillStyle = grd;
        ctx.beginPath();
        ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
        ctx.fill();

        // cull dead
        if (alpha <= 0) {
          particles.splice(i, 1);
        }
      }

      ctx.globalCompositeOperation = 'source-over';
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
      id="fluid"
      className="pointer-events-none fixed inset-0 z-0 mix-blend-screen"
    />
  );
}


