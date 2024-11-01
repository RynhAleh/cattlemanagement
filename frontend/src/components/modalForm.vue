<template>
  <div class="modal-overlay">
		<div class="modal-content" ref="modal" :style="randomPos">
			<div style="">
				<div class="modal-header" ref="header"></div>
				<button class="close-button" @click="close">×</button>
			</div>
			<slot>
				<component :is="innerComponent" />
			</slot>
		</div>
	</div>
</template>

<script>
import { markRaw } from 'vue';
export default {
	data () {
		return {
			innerComponent: null,
			randomPos: '',
		};
	},
  props: {
  	table: String,
  },
	mounted() {
		this.getInnerComponent();
		this.randomPos = `top:${80 + Math.floor(Math.random() * 21)}px;left:${230 + Math.floor(Math.random() * 21)}px;`;
		this.enableDrag(); // Вызываем функцию перетаскивания
	},
  methods: {
    close() {
      this.$emit('close'); // Сигнализирует родителю о закрытии модального окна
    },
		getInnerComponent() {
			import(`./${this.table}/${this.table}Table.vue`).then((module) => {
				this.innerComponent = markRaw(module.default);
			});
		},
		enableDrag() {
			const modal = this.$refs.modal;
			const header = this.$refs.header;

			let offsetX = 0, offsetY = 0;

			const mouseDownHandler = (e) => {
				offsetX = e.clientX - modal.getBoundingClientRect().left;
				offsetY = e.clientY - modal.getBoundingClientRect().top;

				document.addEventListener('mousemove', mouseMoveHandler);
				document.addEventListener('mouseup', mouseUpHandler);
			};

			const mouseMoveHandler = (e) => {
				modal.style.position = 'fixed'; // Убедитесь, что позиция модального окна является абсолютной
				modal.style.left = `${e.clientX - offsetX}px`;
				modal.style.top = `${e.clientY - offsetY}px`;
			};

			const mouseUpHandler = () => {
				document.removeEventListener('mousemove', mouseMoveHandler);
				document.removeEventListener('mouseup', mouseUpHandler);
			};

			header.addEventListener('mousedown', mouseDownHandler);
		}
  },
};
</script>

<style>
/*
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
*/
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.1);
    display: inline-flex;
    justify-content: start;
    align-items: start;
    align-content: center;
    flex-wrap: nowrap;
    flex-direction: column-reverse;
    opacity: 0;
    animation: fadeIn 0.3s ease forwards;
}

.modal-content {
  background: #ffffff;
  padding: 0 20px 20px;
  border-radius: 5px;
  max-width: 80vw;
  /*width: 100%;*/
  position: relative;
  box-shadow: 0px 10px 19px 5px #00000075;
	overflow: auto;
	max-height: 85vh;
  /*transform: scale(0.97);*/
  /*animation: scaleUp 0.3s ease forwards;  Увеличение размера */
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleUp {
  from { transform: scale(0.97); }
  to { transform: scale(1); }
}
.modal-header {
	cursor: move;
	padding: 6px;
}

.close-button {

  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

</style>

