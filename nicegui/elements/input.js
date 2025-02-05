export default {
  template: `
    <q-input
      v-bind="$attrs"
      v-model="inputValue"
      :shadow-text="shadowText"
      @keydown.tab="perform_autocomplete"
      :list="id + '-datalist'"
    >
      <template v-for="(_, slot) in $slots" v-slot:[slot]="slotProps">
        <slot :name="slot" v-bind="slotProps || {}" />
      </template>
    </q-input>
    <datalist v-if="withDatalist" :id="id + '-datalist'">
      <option v-for="option in autocomplete" :value="option"></option>
    </datalist>
  `,
  props: {
    id: String,
    autocomplete: Array,
    value: String,
  },
  data() {
    return {
      inputValue: this.value,
    };
  },
  watch: {
    value(newValue) {
      this.inputValue = newValue;
    },
    inputValue(newValue) {
      this.$emit("update:value", newValue);
    },
  },
  computed: {
    shadowText() {
      if (!this.inputValue) return "";
      const matchingOption = this.autocomplete.find((option) =>
        option.toLowerCase().startsWith(this.inputValue.toLowerCase())
      );
      return matchingOption ? matchingOption.slice(this.inputValue.length) : "";
    },
    withDatalist() {
      const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
      return isMobile && this.autocomplete && this.autocomplete.length > 0;
    },
  },
  methods: {
    perform_autocomplete(e) {
      if (this.shadowText) {
        this.inputValue += this.shadowText;
        e.preventDefault();
      }
    },
  },
};
