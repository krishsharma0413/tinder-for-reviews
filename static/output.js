'use strict';

var tinderContainer = document.querySelector('.tinder');
var allCards = document.querySelectorAll('.tinder--card');
var nope = document.getElementById('nope');
var love = document.getElementById('love');
var neu = document.getElementById('neu');
var cardcontainer = document.querySelector(".tinder--cards");
var lastid = null;
var lastdecision = null;

var sampleCard = `<div data-id="${0}"
    class="tinder--card border-[4px] md:top-[10%] lg:left-[25%] top-[5%] left-[5%] rounded-lg border-background h-[85%] p-8 lg:w-[50%] w-[90%] text-center">
    <div class="w-full h-full flex absolute top-0 left-0 -z-10"
        style="background-image: url(../static/tinder.jpg); background-position: center; background-repeat: no-repeat; background-attachment:fixed; background-size: cover;">
    </div>

    <div class="w-full h-full flex absolute top-0 left-0 -z-10"
        style="background-color: rgba(0, 0, 0, 0.8)">
    </div>

    <h1 class="text-[40px] w-full text-center font-bold text-primary font-sharetechmono">
        ${1}
    </h1>
</div>`;


function decision(chosen, id) {
  fetch('/approve-review?db_id=' + id + '&polarity=' + chosen)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if (data.status == 200) {
        lastid = id;
        lastdecision = chosen;
        // fetch_cards();
      }
    })
  console.log(chosen, id);
}

function undoCard(){
  toggleSettings();
  if(lastid == null) return;
  fetch('/undo-review?id=' + lastid + '&decision=' + lastdecision)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if (data.status == 200) {
        lastid = null;
        
      }
    })

}

function fetch_cards() {
  fetch('/get-reviews')
    .then(response => response.json())
    .then(data => {
      console.log(data);
      cardcontainer.innerHTML = '';
      for (var i = 0; i < data.data.length; i++) {
        cardcontainer.innerHTML += `
          <div data-id="${data.data[i][0]}"
            class="tinder--card border-[4px] md:top-[10%] lg:left-[25%] top-[5%] left-[5%] rounded-lg border-background h-[85%] p-8 lg:w-[50%] w-[90%] text-center">
            <div class="w-full h-full flex absolute top-0 left-0 -z-10"
              style="background-image: url(../static/tinder.jpg); background-position: center; background-repeat: no-repeat; background-attachment:fixed; background-size: cover;">
            </div>
            <div class="w-full h-full flex absolute top-0 left-0 -z-10"
              style="background-color: rgba(0, 0, 0, 0.8)">
            </div>
            <h1 class="text-[40px] w-full text-center font-bold text-primary font-sharetechmono">
              ${data.data[i][1]}
            </h1>
          </div>`;
      }
      initCards();
      var allCards = document.querySelectorAll('.tinder--card');

      allCards.forEach(function (el) {
        var hammertime = new Hammer(el);

        hammertime.on('pan', function (event) {
          el.classList.add('moving');
        });

        hammertime.on('pan', function (event) {
          if (event.deltaX === 0) return;
          if (event.center.x === 0 && event.center.y === 0) return;

          tinderContainer.classList.toggle('tinder_love', event.deltaX > 0);
          tinderContainer.classList.toggle('tinder_nope', event.deltaX < 0);

          var xMulti = event.deltaX * 0.03;
          var yMulti = event.deltaY / 80;
          var rotate = xMulti * yMulti;

          event.target.style.transform = 'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';
        });

        hammertime.on('panend', function (event) {
          el.classList.remove('moving');
          tinderContainer.classList.remove('tinder_love');
          tinderContainer.classList.remove('tinder_nope');

          var moveOutWidth = document.body.clientWidth;
          var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;

          event.target.classList.toggle('removed', !keep);

          if (keep) {
            event.target.style.transform = '';
          } else {
            var endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth);
            var toX = event.deltaX > 0 ? endX : -endX;
            var endY = Math.abs(event.velocityY) * moveOutWidth;
            var toY = event.deltaY > 0 ? endY : -endY;
            var xMulti = event.deltaX * 0.03;
            var yMulti = event.deltaY / 80;
            var rotate = xMulti * yMulti;

            event.target.style.transform = 'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';
            initCards();
            decision((toX > 0) ? 1 : -1, el.getAttribute("data-id"));
          }
        });
      });
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function initCards() {
  var newCards = document.querySelectorAll('.tinder--card:not(.removed)');
  var allCards = document.querySelectorAll('.tinder--card');

  if (newCards.length == 0) {
    console.log('No new cards. Fetching more cards...');
    fetch_cards();
    return;
  }

  newCards.forEach(function (card, index) {
    card.style.zIndex = allCards.length - index;
    card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
    card.style.opacity = (10 - index) / 10;
  });

  tinderContainer.classList.add('loaded');
}

initCards();

allCards.forEach(function (el) {
  var hammertime = new Hammer(el);

  hammertime.on('pan', function (event) {
    el.classList.add('moving');
  });

  hammertime.on('pan', function (event) {
    if (event.deltaX === 0) return;
    if (event.center.x === 0 && event.center.y === 0) return;

    tinderContainer.classList.toggle('tinder_love', event.deltaX > 0);
    tinderContainer.classList.toggle('tinder_nope', event.deltaX < 0);

    var xMulti = event.deltaX * 0.03;
    var yMulti = event.deltaY / 80;
    var rotate = xMulti * yMulti;

    event.target.style.transform = 'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';
  });

  hammertime.on('panend', function (event) {
    el.classList.remove('moving');
    tinderContainer.classList.remove('tinder_love');
    tinderContainer.classList.remove('tinder_nope');

    var moveOutWidth = document.body.clientWidth;
    var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;

    event.target.classList.toggle('removed', !keep);

    if (keep) {
      event.target.style.transform = '';
    } else {
      var endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth);
      var toX = event.deltaX > 0 ? endX : -endX;
      var endY = Math.abs(event.velocityY) * moveOutWidth;
      var toY = event.deltaY > 0 ? endY : -endY;
      var xMulti = event.deltaX * 0.03;
      var yMulti = event.deltaY / 80;
      var rotate = xMulti * yMulti;

      event.target.style.transform = 'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';
      initCards();
      decision((toX > 0) ? 1 : -1, el.getAttribute("data-id"));
    }
  });
});

function createButtonListener(love) {
  return function (event) {
    var cards = document.querySelectorAll('.tinder--card:not(.removed)');
    var moveOutWidth = document.body.clientWidth * 1.5;

    if (!cards.length) return false;

    var card = cards[0];

    card.classList.add('removed');

    if (love == 1) {
      card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
    } else if (love == -1) {
      card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
    } else if (love == 0) {
      card.style.transform = 'translate( 0px, -' + moveOutWidth + 'px) rotate(30deg)';
    }

    initCards();

    decision(love, card.getAttribute("data-id"));

    event.preventDefault();
  };
}

function toggleSettings() {
  var settings = document.getElementById("settings-dialog");
  settings.classList.toggle("hidden");
}

var nopeListener = createButtonListener(-1);
var loveListener = createButtonListener(1);
var neuListener = createButtonListener(0);

nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);
neu.addEventListener('click', neuListener);
