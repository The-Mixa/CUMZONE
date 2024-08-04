const darkBackground = document.querySelector('.background-dark');
const deliteButton = document.querySelector('.delite');
const notDeliteBUtton = document.querySelector('.not-delite');
const deliteMenu = document.querySelector('.delite-form');
const id_del_field = document.querySelector('.id-for-delite');

notDeliteBUtton.addEventListener('click', () => {
    darkBackground.toggleAttribute('hidden');
    deliteMenu.toggleAttribute('hidden');
});
 
deliteButton.addEventListener('click', () => {
    darkBackground.toggleAttribute('hidden');
    deliteMenu.toggleAttribute('hidden');
    deliteProduct(id_del_field.innerHTML);
    const product = document.querySelector(`#product-${id_del_field.innerHTML}`);
    product.toggleAttribute('hidden');
});

function deliteProduct(productId) {
    fetch(`/delite_product548548/${productId}`,
        { method: 'POST' }
    )
}