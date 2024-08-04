const saveBtn = document.querySelector('.save-comment-button');
const makeCommentBlock = document.querySelector('.make-comments-block');
const textarea = document.querySelector('.textarea');


saveBtn.addEventListener('click', () => {
    makeCommentBlock.toggleAttribute('hidden');
    const comments = document.querySelector('.comments');
    const comment = createComment(textarea.value);
    comments.appendChild(comment);
});

function makeComment(productId, curUsId) {
    fetch(`/save_comment548548/${productId}/${curUsId}/${textarea.value}`,
        { method: 'POST' }
    )
}

const createComment = (text) => {
    // Создаем корневой элемент комментария
    const comment = document.createElement('div');
    comment.classList.add('comment');
    comment.style.margin = '5px';
    comment.style.backgroundColor = '#444';
    comment.style.borderRadius = '15px';
    comment.style.padding = '5px';

    // Создаем секцию с информацией о пользователе и оценкой
    const header = document.createElement('div');
    header.style.display = 'flex';
    header.style.flexDirection = 'row';
    header.style.justifyContent = 'space-between';
    header.style.marginRight = '50px';
    header.style.flexWrap = 'wrap';

    // Создаем секцию с изображением пользователя и информацией о нем
    const userInfo = document.createElement('div');
    userInfo.style.display = 'flex';
    userInfo.style.flexDirection = 'row';

    // Создаем изображение пользователя
    const userImage = document.createElement('div');
    userImage.classList.add('comment-author-image');
    userImage.style.marginRight = '20px';
    const userImageElement = document.createElement('img');
    userImageElement.style.width = '50px';
    userImageElement.style.height = '50px';
    userImageElement.style.borderRadius = '25px';
    userImageElement.src = document.querySelector('#current_user-profile_image').innerHTML;
    userImage.appendChild(userImageElement);

    // Создаем информацию о пользователе
    const authorInfo = document.createElement('div');
    authorInfo.classList.add('comment-author-info');
    const authorName = document.createElement('p');
    authorName.style.fontSize = '20px';
    authorName.textContent = document.querySelector('#current_user-nickname').innerHTML;
    const authorDate = document.createElement('p');
    authorDate.style.color = 'grey';
    authorDate.textContent = document.querySelector('#date_now').innerHTML;
    authorInfo.appendChild(authorName);
    authorInfo.appendChild(authorDate);

    // Добавляем изображение пользователя и информацию о нем в секцию с пользователем
    userInfo.appendChild(userImage);
    userInfo.appendChild(authorInfo);

    // Создаем секцию с оценкой комментария
    const ratingContainer = document.createElement('div');
    ratingContainer.classList.add('comment-rating');

    

    // Добавляем секции с пользователем и оценкой в верхнюю часть комментария
    header.appendChild(userInfo);
    header.appendChild(ratingContainer);

    // Создаем секцию с текстом комментария
    const commentText = document.createElement('div');
    commentText.classList.add('comment-text');
    const commentTextElement = document.createElement('p');
    commentTextElement.textContent = text;
    commentText.appendChild(commentTextElement);

    // Добавляем секцию с текстом комментария в корневой элемент
    comment.appendChild(header);
    comment.appendChild(commentText);

    // Возвращаем созданный элемент комментария
    return comment;
};

