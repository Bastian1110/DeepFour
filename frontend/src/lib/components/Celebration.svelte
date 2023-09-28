<script lang="ts">
  import { Confetti } from "svelte-confetti";
  export let triger = false;
  export let show = false;

  const showConfetti = () => {
    show = false;
    console.log(show);
    setTimeout(() => {
      show = false;
      console.log(show);
    }, 2000);
  };

  $: {
    if (triger) showConfetti;
  }
</script>

{#if show}
  <div
    style="position: fixed; top: -50px; left: 0; height: 100vh; width: 100vw; display: flex; justify-content: center; overflow: hidden;"
  >
    <Confetti
      x={[-5, 5]}
      y={[0, 0.1]}
      delay={[0, 1500]}
      duration={2000}
      amount={1000}
      fallDistance="70vh"
      size={30}
    />
  </div>
{/if}
