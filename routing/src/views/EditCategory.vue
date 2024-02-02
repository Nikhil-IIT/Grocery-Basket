<template>
    <div>
        <form @submit="handleSaving">

            <div class="form-group">
                <label for="exampleFormControlTextarea1">Name:</label>
                <textarea v-model="category.c_name" class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Save</button>
        </form>
    </div>
</template>


<script>
import axios from 'axios';
  
  export default {
    data() {
      return {
        category: {
          c_name: '',
        },
      };
    },
  
    methods: {
      getdata() {
        const categoryId = this.$route.params.id;
        const path = `http://localhost:5000/edit_category/${categoryId}`;
        axios
          .get(path)
          .then((res) => {
            const categoryData = res.data.items[0];
            console.log(categoryData)
            this.category = { ...this.category, ...categoryData };
          })
          .catch((error) => {
            console.error('ERROR:', error.message);
          });
      },
  
      async handleSaving(event) {
      event.preventDefault();
      try {
        const categoryId = this.$route.params.id;
        const response = await axios.post(`http://localhost:5000/edit_category/${categoryId}`, this.category);
        console.log('Saving successful:', response.data.message);
        this.initForm();
        this.$router.push('/admin_panel');
        }catch (error) {
          console.error('Saving failed:', error.message);
        }
      },
  
      initForm() {
        this.category.c_name="";
      },
    },
    created() {
      this.getdata();
    },
  };
</script>