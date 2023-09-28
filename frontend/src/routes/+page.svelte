<script lang="ts">
  import { onMount } from "svelte";
  import { Piece } from "$lib/components";
  import { Confetti } from "svelte-confetti";

  let player = 1;
  type Matrix = number[][];
  let matrix: Matrix = Array(6)
    .fill(null)
    .map(() => Array(7).fill(0));
  let done = false;

  const updateGameState = async () => {
    try {
      const response = await fetch("http://localhost:8082/game-state");
      const data = await response.json();
      matrix = data.board;
      if (player == 2) {
        await handleRobotAction();
      }
    } catch (err) {
      console.log(err);
    }
  };

  const resetGame = async () => {
    try {
      await fetch("http://localhost:8082/reset");
      player = 1;
      updateGameState();
    } catch (err) {
      console.log(err);
    }
  };

  const handleHumanAction = async (id: number) => {
    try {
      let response = await fetch("http://localhost:8082/make-action", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ action: id }),
      });
      const data = await response.json();
      console.log(data);
      if (data.done) {
        triggerConfetti();
      }
      putPiece(id);
    } catch (err) {
      console.log(err);
    }
  };

  const handleRobotAction = async () => {
    try {
      let response = await fetch("http://localhost:8082/agent-action");
      let data = await response.json();
      actualColumn = data.info.action;
      setTimeout(() => {
        putPiece(data.info.action);
      }, 1200);
    } catch (err) {
      console.log(err);
    }
  };

  const triggerConfetti = () => {
    done = true;
    console.log(done);
    setTimeout(() => {
      done = false;
    }, 2500);
  };

  let actualColumn: number | null = null;
  const handleColumnHover = (col: number) => {
    actualColumn = col;
  };

  const putPiece = (col: number) => {
    let row = matrix.length - 1;
    while (row >= 0 && matrix[row][col] !== 0) {
      row--;
    }
    if (row === -1) return;

    const topPieceElement = document.querySelector(
      `[data-top-piece-id="${col}"]`
    ) as HTMLElement;

    const destinyPieceElement = document.querySelector(
      `[data-piece-col="${col}"][data-piece-row="${row}"]`
    ) as HTMLElement;

    const { top, left } = destinyPieceElement.getBoundingClientRect();
    const { top: pieceTop, left: pieceLeft } =
      topPieceElement.getBoundingClientRect();

    const translateX = left - pieceLeft;
    const translateY = top - pieceTop;

    topPieceElement.style.transition = "transform 0.5s ease-in";
    topPieceElement.style.transform = `translate(${translateX}px, ${translateY}px)`;

    setTimeout(() => {
      topPieceElement.style.transition = "";
      topPieceElement.style.transform = "";
      matrix[row][col] = player;
      matrix = [...matrix];
      player = player == 2 ? 1 : 2;
      updateGameState();
    }, 500);
  };
  onMount(updateGameState);
</script>

<main
  class="grid grid-cols-3 grid-rows-3 w-screen h-screen text-white"
  style="grid-template-columns: 25% 50% 25%; grid-template-rows: 5% 65% 15%;"
>
  <div class="col-start-1 row-span-3 text-center">
    <button
      on:click={resetGame}
      class="border-violet-500 border-2 text-white font-bold px-6 py-2 rounded-sm hover:scale-105 active:bg-violet-700 transition-all duration-300 mt-[60%]"
    >
      Reset Game
    </button>
    <button
      on:click={handleRobotAction}
      class="border-violet-500 border-2 text-white font-bold px-6 py-2 rounded-sm hover:scale-105 active:bg-violet-700 transition-all duration-300 mt-[60%]"
    >
      Test
    </button>
  </div>

  <div class="col-start-2 row-start-2">
    <div class="flex justify-between px-5 py-1">
      <Piece state={actualColumn == 0 ? player : 0} data-top-piece-id={0} />
      <Piece state={actualColumn == 1 ? player : 0} data-top-piece-id={1} />
      <Piece state={actualColumn == 2 ? player : 0} data-top-piece-id={2} />
      <Piece state={actualColumn == 3 ? player : 0} data-top-piece-id={3} />
      <Piece state={actualColumn == 4 ? player : 0} data-top-piece-id={4} />
      <Piece state={actualColumn == 5 ? player : 0} data-top-piece-id={5} />
      <Piece state={actualColumn == 6 ? player : 0} data-top-piece-id={6} />
    </div>
    <div class="bg-slate-800 rounded-xl grid grid-rows-7 gap-2 text-black p-5">
      {#each matrix as row, rowIndex}
        <div class="flex justify-between">
          {#each row as item, columnIndex}
            <Piece
              state={item}
              column={columnIndex}
              onClick={handleHumanAction}
              onHover={handleColumnHover}
              data-piece-col={columnIndex}
              data-piece-row={rowIndex}
            />
          {/each}
        </div>
      {/each}
    </div>
  </div>
</main>

{#if done}
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
