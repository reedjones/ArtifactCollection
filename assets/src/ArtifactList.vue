<template>
  <div class="card">
    <div v-if="isLoading()">
      <div class="border-round border-1 surface-border p-4 surface-card">
        <ul class="m-0 p-0 list-none">
          <li class="mb-3">
            <div class="flex">
              <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
              <div class="align-self-center" style="flex: 1">
                <Skeleton width="100%" class="mb-2"></Skeleton>
                <Skeleton width="75%"></Skeleton>
              </div>
            </div>
          </li>
          <li class="mb-3">
            <div class="flex">
              <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
              <div class="align-self-center" style="flex: 1">
                <Skeleton width="100%" class="mb-2"></Skeleton>
                <Skeleton width="75%"></Skeleton>
              </div>
            </div>
          </li>
          <li class="mb-3">
            <div class="flex">
              <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
              <div class="align-self-center" style="flex: 1">
                <Skeleton width="100%" class="mb-2"></Skeleton>
                <Skeleton width="75%"></Skeleton>
              </div>
            </div>
          </li>
          <li>
            <div class="flex">
              <Skeleton shape="circle" size="4rem" class="mr-2"></Skeleton>
              <div class="align-self-center" style="flex: 1">
                <Skeleton width="100%" class="mb-2"></Skeleton>
                <Skeleton width="75%"></Skeleton>
              </div>
            </div>
          </li>
        </ul>
      </div>

    </div>

    <DataView :value="artifacts" :sortOrder="sortOrder"
              :sortField="sortField" :layout="layout"
              @page="onDataViewPageEvent($event)" paginator
              :rows="pagination.objects_count"
              :total-records="pagination.total_pages"
              :rowsPerPageOptions="[10, 20, 30]"
              :current_page="pagination.current_page"
              :first="pagination.first"
              class="fadeinleft animation-fill-forwards" v-if="dataLoaded()">
      <template #header>

        <div class="flex justify-content-between">
          <Dropdown v-model="sortKey" :options="sortOptions"
                    optionLabel="label" placeholder="Sort By Id"
                    @change="onSortChange($event)"/>


          <div v-if="states">
            <MultiSelect v-model="selectedStates" :options="states"
                         optionLabel="name" placeholder="Select State(s)"
                         display="chip" class="w-full md:w-20rem" @change="onSelectedStateChange($event)">
              <template #option="slotProps">
                <div class="flex align-items-center">

                  <img :alt="slotProps.option.name"
                       :src="'http://127.0.0.1:8000' + slotProps.option.flag" :class="`mr-2`"
                       style="width: 18px"/>


                  <div>{{ slotProps.option.name }}</div>
                </div>
              </template>
              <template #footer>
                <div class="py-2 px-3">
                  <b>{{ selectedStates ? selectedStates.length : 0 }}</b>
                  item{{ (selectedStates ? selectedStates.length : 0) > 1 ? 's' : '' }} selected.
                </div>
              </template>
            </MultiSelect>
          </div>
          <div v-else>
            <MultiSelect placeholder="Loading States..." loading class="w-full md:w-20rem"></MultiSelect>
          </div>


          <div class="ml-auto">
            <DataViewLayoutOptions v-model="layout"/>
          </div>
        </div>
      </template>

      <template #list="slotProps">

        <div class="grid grid-nogutter">
          <div v-for="(item, index) in slotProps.items" :key="index" class="col-12">
            <div class="flex flex-column xl:flex-row xl:align-items-start p-4 gap-4"
                 :class="{ 'border-top-1 surface-border': index !== 0 }">
              <img class="w-9 sm:w-16rem xl:w-10rem shadow-2 block xl:block mx-auto border-round"
                   :src="`https://harpercollection.info/uploads/${item.photo_url}`" :alt="item.id"/>
              <div
                  class="flex flex-column sm:flex-row justify-content-between align-items-center xl:align-items-start flex-1 gap-4">
                <div class="flex flex-column align-items-center sm:align-items-start gap-3">
                  <div class="text-2xl font-bold text-900">Item Number: {{ item.aw_item_number }}</div>
                  <!--                  <Rating :modelValue="item.rating" readonly :cancel="false"></Rating>-->
                  <div class="flex align-items-center gap-3">
                                        <span class="flex align-items-center gap-2">
                                            <i class="pi pi-tag"></i>
                                            <span class="font-semibold">{{ item.maincategory }}</span>
                                        </span>
                    <Tag :value="item.subcategory"></Tag>
                    <Tag :value="item.category_attribute"></Tag>
                  </div>
                </div>
                <div class="flex sm:flex-column align-items-center sm:align-items-end gap-3 sm:gap-2">

                  <Button icon="pi pi-pi-circle-fill" rounded value="Hello"></Button>
                </div>
              </div>
            </div>
          </div>
        </div>


      </template>

      <template #grid="slotProps">


        <div class="grid grid-nogutter">
          <div v-for="(item, index) in slotProps.items" :key="index" class="col-12 sm:col-6 lg:col-12 xl:col-4 p-2">
            <div class="p-4 border-1 surface-border surface-card border-round">
              <div class="flex flex-wrap align-items-center justify-content-between gap-2">
                <div class="flex align-items-center gap-2">
                  <Tag style="background: linear-gradient(to right, var(--primary-300), var(--primary-700))">
                    <div class="flex align-items-center gap-2">
                      <img :alt="item.from_state" :src="getFlag(item.from_state)" class="" style="width: 18px"/>
                      <span class="text-base">{{ item.from_state }}</span>
                      <i class="pi pi-times text-xs"></i>
                    </div>
                  </Tag>
                </div>

                <div class="ml-auto flex gap-1">
                  <Tag :value="item.maincategory"/>

                  <Tag :value="item.subcategory"/>


                  <Tag :value="item.category_attribute"/>

                </div>


                <!--                <Tag :value="item.maincategory"></Tag>-->
                <!--                <Tag :value="item.subcategory"></Tag>-->
                <!--                <Tag :value="item.category_attribute"></Tag>-->
              </div>
              <div class="flex flex-column align-items-center gap-3 py-5">
                <img class="w-9 shadow-2 border-round"
                     :src="`https://harpercollection.info/uploads/${item.photo_url}`"
                     :alt="item.name"/>
                <div class="text-2xl font-bold">Item: {{ item.aw_item_number }}</div>
              </div>
              <div class="flex align-items-center justify-content-between">
                <Button icon="pi pi-pi-circle-fill" rounded value="Hello"></Button>
              </div>
            </div>
          </div>
        </div>

      </template>


    </DataView>


  </div>


</template>

<script>
import CategoryService from '@/service/CategoryService';
import MaterialService from '@/service/MaterialService';
import CountyService from '@/service/CountryService';
import StateService from '@/service/StateService';
import ArtifactService from '@/service/ArtifactService';

export default {
  data() {
    return {
      artifacts: null,
      artifacts_service: null,
      pagination: {
        object_count: 0,
        total_pages:0,
        current_page:0,
        first:0
      },
      selectedStates: null,
      states: null,
      sortKey: null,
      sortOrder: null,
      sortField: null,
      layout: 'grid',
      sortOptions: [
        {label: 'ID#', value: '!id'},
        {label: 'ID# Reverse', value: 'id'}
      ]
    };
  },
  mounted() {
    this.artifact_service = new ArtifactService();
    const state_service = new StateService();
    this.fetchArtifacts({'page':1})


    state_service.getStates().then((data) => {
      this.states = data['states'].map((s) => {
        return {
          'name': s.name,
          'flag': s.flag.split(" ").join("_"),
          'id': s.id
        }
      });
      console.log(data)
    })
  },
  methods: {
    getFlag(name) {
      return "http://127.0.0.1:8000/static/flags/Flag_of_" + name.split(" ").join("_") + ".svg"
    },
    isLoading() {
      return this.artifacts == null
    },
    dataLoaded(){return ! this.isLoading()},
    fetchArtifacts(params){
      this.artifacts = null;
      this.pagination = null;
      console.log(`set artifacts... data loaded: ${this.dataLoaded()}`)

      this.artifact_service.getDataListSimple(params).then((data) => {
        //this.artifacts = data['artifacts'];
        this.pagination = data['pagination'];
        this.artifacts = data['artifacts'];
        console.log(`done set artifacts... data loaded: ${this.dataLoaded()}`)

      })
    },
    getCategoryTree(item) {
      let tree = {
        "root": [{
          key: "0",
          label: item.maincategory,
          data: item.maincategory,
          children: []

        }]
      }
      if (item.subcategory) {
        tree['root'][0]['children'].push({
          key: "0-0",
          label: item.subcategory,
          data: item.subcategory,
          children: []
        })

        if (item.category_attribute) {
          tree['root'][0]['children'].push(
              {
                key: "0-1",
                label: item.category_attribute,
                data: item.category_attribute
              }
          )
        }

      }
      console.log(tree)
      return tree.root
    },
    getSeverity(product) {
      switch (product.inventoryStatus) {
        case 'INSTOCK':
          return 'success';

        case 'LOWSTOCK':
          return 'warning';

        case 'OUTOFSTOCK':
          return 'danger';

        default:
          return null;
      }
    },
    onSortChange(event) {
      const value = event.value.value;
      const sortValue = event.value;

      if (value.indexOf('!') === 0) {
        this.sortOrder = -1;
        this.sortField = value.substring(1, value.length);
        this.sortKey = sortValue;
      } else {
        this.sortOrder = 1;
        this.sortField = value;
        this.sortKey = sortValue;
      }
    },
    onDataViewPageEvent(event) {
      //DataViewPageEvent
      this.pagination.first += 10;
      this.pagination.current_page = event.page + 1 ;
      console.log(`Page changed currently ${event.page}`);
      const page = event.page + 1;
      this.fetchArtifacts({'page':page})

    },
    onSelectedStateChanged(event){
     const query = {"states__in" : this.selectedStates}

    }


  }
};
</script>


<style>
/* Add your styles here */


</style>