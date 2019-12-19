class PageCutter{

    /**
     *
     * @param rowList {rowList:[], active:0}
     */
    constructor(rowList){
        this.rowList = rowList;
        this.cuttedRowList = this.rowList;
        this.limit = 10;
        this.offset = 0;
        this.cutPage();
    }

    setLimit(limit){
        this.limit = limit;
        this.offset = 0;
        this.cutPage();
    }

    getLimit(){
        return this.limit;
    }

    cutPage(){
        this.cuttedRowList = this.rowList.slice(this.offset, this.offset + this.limit);
    }
    onGoPrev(){

        if(this.offset - this.limit >= 0){
            this.offset -= this.limit;
        }else{
            this.offset = 0;
        }

        this.cutPage();
    }
    onGoNext(){
        if(this.offset + this.limit <= this.rowList.length){
            this.offset += this.limit;
        }
        this.cutPage();
    }
    getRowList(){
        return this.cuttedRowList;
    }
}
