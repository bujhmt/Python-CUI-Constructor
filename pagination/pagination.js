//https://github.com/bujhmt/utils for suggestions and corrections

//max number of elements per page
const maxPageSize = 100
//default one page size
const defaultPageSize = 10

/** Simple function for pagination
 *
 * @param {String | Number} page - page number as a string or number
 * @param {String | Number} per_page - number of items on this page
 * @param {Array<any>} itemsArray - the collection to paginate
 * @return {Array<any>} - a collection of elements that met the pagination condition
 */
function getResPageItems(page, per_page, itemsArray) {
    if (itemsArray.length === 0) 
        return itemsArray
    
    if (!page || !per_page) {
        itemsArray.splice(defaultPageSize)
        return itemsArray
    }
        
    try {
        page = Number(page)
        per_page = Number(per_page)
    } catch(err) {
        itemsArray.splice(defaultPageSize)
        return itemsArray
    }
    
    if (per_page < 1)
        per_page = defaultPageSize

    if (per_page > maxPageSize)
        per_page = maxPageSize
        
    const pageCount = Math.ceil(itemsArray.length / per_page)

    if (page < 1) {
        itemsArray.splice(defaultPageSize)
        return itemsArray
    }

    if (page > pageCount) {
        return itemsArray.splice(itemsArray.length - per_page)
    } 
        
    return itemsArray.splice((page - 1) * per_page, per_page)
}

module.exports = getResPageItems