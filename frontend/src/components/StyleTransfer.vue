<script setup>
import { ref } from "vue";
import axios from "axios";

const sourceImage = ref(null);
const styleImage = ref(null);
const resImageId = ref(null);
const getImagePath = ref(null);
const loading = ref(false);

function handleImage(e, source) {
  try {
    if (e.target.files[0].size > 2097152) {
      alert("File too large");
    } else {
      toBase64(e.target.files[0]).then((res) =>
        source ? (sourceImage.value = res) : (styleImage.value = res)
      );
    }
  } catch (error) {}
}

const toBase64 = (file) =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject();
  });

const getImage = () => {
  if (sourceImage.value && styleImage.value) {
    getImagePath.value = null;
    resImageId.value = null;
    loading.value = true;
    axios
      .post(
        `${window.location.protocol}//${window.location.hostname}/api/createImage`,
        {
          content_image_url: sourceImage.value,
          style_image_url: styleImage.value,
        }
      )
      .then(function (response) {
        getImagePath.value = `${window.location.protocol}//${window.location.hostname}/api/image/?id=${response.data}`;
        resImageId.value = response.data;
      })
      .finally(() => {
        loading.value = false;
      });
  }
};
</script>

<template>
  <div class="flex flex-col w-[1000px] space-y-6 items-center">
    <div>
      <h1 class="title">Style Transfer</h1>
      <h2 class="subtitle">
        using
        <a
          class="subtitle text-pink-500"
          href="https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
        >
          magenta</a
        >
      </h2>
      <h2 class="text-xl">by Abi</h2>
    </div>

    <div class="flex justify-around space-x-6 items-center">
      <div class="card">
        <h2 class="subtitle">Source Image</h2>
        <label class="btn btn-blue inline-block">
          UPLOAD
          <input
            class="hidden"
            type="file"
            @change="handleImage($event, true)"
            accept="image/png, image/jpeg"
          />
        </label>

        <img
          v-if="sourceImage"
          class="object-cover h-80 border-0"
          v-bind:src="sourceImage"
          alt=""
        />
      </div>

      <div class="card">
        <h2 class="subtitle">Style Image</h2>
        <label class="btn btn-blue inline-block">
          UPLOAD
          <input
            class="hidden"
            type="file"
            @change="handleImage($event, false)"
            accept="image/png, image/jpeg"
          />
        </label>
        <img
          v-if="styleImage"
          class="h-80 object-cover"
          v-bind:src="styleImage"
          alt=""
        />
      </div>
      <button
        class="btn btn-blue"
        @click="getImage"
        :disabled="!sourceImage || !styleImage || loading"
      >
        CREATE
      </button>
      <div class="card">
        <h2 class="subtitle">Resulting Image</h2>
        <div v-if="loading" id="spinner" class="text-center self-center">
          <div
            class="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-64 w-64"
          ></div>
        </div>

        <img
          v-if="resImageId"
          :src="getImagePath"
          alt=""
          class="h-80 object-cover"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.btn {
  @apply font-bold py-2 px-4 rounded cursor-pointer disabled:cursor-default;
}
.btn-blue {
  @apply bg-blue-500 text-white disabled:bg-slate-500;
}
.btn-blue:hover {
  @apply bg-blue-700 disabled:bg-slate-500;
}
.title {
  @apply text-8xl font-semibold;
}
.subtitle {
  @apply text-xl font-semibold;
}
.card {
  @apply h-[500px] w-96 shadow-2xl p-6 space-y-3 flex flex-col;
}

.loader {
  border-top-color: #3498db;
  -webkit-animation: spinner 1.5s linear infinite;
  animation: spinner 1.5s linear infinite;
}

@-webkit-keyframes spinner {
  0% {
    -webkit-transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
  }
}

@keyframes spinner {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
