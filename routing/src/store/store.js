import { createStore } from 'vuex';

const store = createStore({
    state: {
        userLoggedIn: false,
        Smloggedin:false,
        filteredProducts: [],
        sm_id:0,
    },
    mutations: {
        setSmid(state, id) {
            state.sm_id = id;
            },

        setUserLoggedIn(state, loggedIn) {
        state.userLoggedIn = loggedIn;
        },

        setSmloggedin(state, loggedIn) {
            state.Smloggedin = loggedIn;
        },
        
        setFilteredProducts(state, data) {
            state.filteredProducts = data;
        },
    },

    actions: {
        updateSmid({ commit }, newValue) {
            commit('setSmid', newValue);
        },
    },
    
    getters: {
        getSmid: (state) => state.sm_id,
    },
});

export default store;