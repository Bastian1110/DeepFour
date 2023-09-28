<script lang="ts">
  export let state = 0;
  export let onClick = (col: number) => {};
  export let onHover = (col: number) => {};
  export let column = 0;
  export let style = "";
  type ColorsDict = {
    [key: number]: string;
  };

  const numberToColor: ColorsDict = {
    0: "bg-black",
    1: "bg-teal-500",
    2: "bg-indigo-500",
    3: "bg-transparent",
  };
</script>

<div
  tabindex="0"
  role="button"
  {...$$props}
  on:click={() => onClick(column)}
  on:mouseover={() => onHover(column)}
  on:focus={() => onHover(column)}
  class="rounded-full w-16 h-16 inline-bloc {numberToColor[state]} {style}"
/>
