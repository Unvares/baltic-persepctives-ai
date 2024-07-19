import lottie from 'lottie-web';
import type { AnimationItem } from 'lottie-web';

export function useLogoAnimation(ref: Ref, data: any, autoplay: boolean = true): AnimationItem | null {
  if (!ref.value) return null;

  const params = {
    container: ref.value,
    loop: true,
    autoplay,
    animationData: data,
  };

  const anim = lottie.loadAnimation(params);
  anim.addEventListener("loopComplete", () => anim.stop());
  ref.value.addEventListener("mouseover", () => anim.play());

  return anim;
}
