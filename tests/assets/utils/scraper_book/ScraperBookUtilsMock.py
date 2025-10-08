from typing import Any

import httpx
import respx

from src.domain.scrape_book.ScrapeBook import ScrapeBook
from src.domain.scrape_book.vos.Money import Money
from src.domain.scrape_book.vos.Rating import Rating
from src.domain.scrape_book.vos.Upc import Upc
from src.standard.built_in.Static import Static

page_1_html = """
<div class="col-sm-8 col-md-9">
  <div class="page-header action">
    <h1>All products</h1>
  </div>
  <div id="messages"></div>
  <div id="promotions"></div>
  <form method="get" class="form-horizontal">
    <div style="display:none"></div>
    <strong>1000</strong> results - showing <strong>1</strong> to <strong>20</strong>.
  </form>
  <section>
    <div class="alert alert-warning" role="alert"><strong>Warning!</strong> This is a demo website for web scraping purposes. Prices and ratings here were randomly assigned and have no real meaning.</div>
    <div>
      <ol class="row">
        <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
          <article class="product_pod">
            <div class="image_container">
              <a href="catalogue/a-light-in-the-attic_1000/index.html"><img src="media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg" alt="A Light in the Attic" class="thumbnail"></a>
            </div>
            <p class="star-rating Three">
              <i class="icon-star"></i>
              <i class="icon-star"></i>
              <i class="icon-star"></i>
              <i class="icon-star"></i>
              <i class="icon-star"></i>
            </p>
            <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a></h3>
            <div class="product_price">
              <p class="price_color">£51.77</p>
              <p class="instock availability"><i class="icon-ok"></i> In stock</p>
              <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
            </div>
          </article>
        </li>
        <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
          <article class="product_pod">
            <div class="image_container">
              <a href="catalogue/tipping-the-velvet_999/index.html"><img src="media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg" alt="Tipping the Velvet" class="thumbnail"></a>
            </div>
            <p class="star-rating One">
              <i class="icon-star"></i>
              <i class="icon-star"></i>
              <i class="icon-star"></i>
              <i class="icon-star"></i>
              <i class="icon-star"></i>
            </p>
            <h3><a href="catalogue/tipping-the-velvet_999/index.html" title="Tipping the Velvet">Tipping the Velvet</a></h3>
            <div class="product_price">
              <p class="price_color">£53.74</p>
              <p class="instock availability"><i class="icon-ok"></i> In stock</p>
              <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
            </div>
          </article>
        </li>      
      </ol>
      <div>
        <ul class="pager">
          <li class="current">Page 1 of 2</li>
          <li class="next"><a href="catalogue/page-2.html">next</a></li>
        </ul>
      </div>
    </div>
  </section>
</div>
"""

page_2_html = """
<div class="col-sm-8 col-md-9">
  <div class="page-header action">
    <h1>All products</h1>
  </div>

  <div id="messages"></div>
  <div id="promotions"></div>

  <form method="get" class="form-horizontal">
    <div style="display:none"></div>
    <strong>1000</strong> results - showing <strong>981</strong> to <strong>1000</strong>.
  </form>

  <section>
    <div class="alert alert-warning" role="alert">
      <strong>Warning!</strong> This is a demo website for web scraping purposes. Prices and ratings here were randomly assigned and have no real meaning.
    </div>

    <div>
      <ol class="row">
        <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
          <article class="product_pod">
            <div class="image_container">
              <a href="frankenstein_20/index.html">
                <img src="../media/cache/00/25/0025515e987a1ebd648773f9ac70bfe6.jpg" alt="Frankenstein" class="thumbnail">
              </a>
            </div>
            <p class="star-rating Two"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
            <h3><a href="frankenstein_20/index.html" title="Frankenstein">Frankenstein</a></h3>
            <div class="product_price">
              <p class="price_color">£38.00</p>
              <p class="instock availability"><i class="icon-ok"></i> In stock</p>
              <form>
                <button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button>
              </form>
            </div>
          </article>
        </li>
        <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
          <article class="product_pod">
            <div class="image_container">
              <a href="forever-rockers-the-rocker-12_19/index.html">
                <img src="../media/cache/7f/b0/7fb03a053c270000667a50dd8d594843.jpg" alt="Forever Rockers (The Rocker #12)" class="thumbnail">
              </a>
            </div>
            <p class="star-rating Three"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
            <h3><a href="forever-rockers-the-rocker-12_19/index.html" title="Forever Rockers (The Rocker #12)">Forever Rockers (The Rocker ...)</a></h3>
            <div class="product_price">
              <p class="price_color">£28.80</p>
              <p class="instock availability"><i class="icon-ok"></i> In stock</p>
              <form>
                <button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button>
              </form>
            </div>
          </article>
        </li>
      </ol>

      <div>
        <ul class="pager">
          <li class="previous"><a href="catalogue/page-1.html">previous</a></li>
          <li class="current">Page 2 of 2</li>
        </ul>
      </div>
    </div>
  </section>
</div>
"""

content_page_1_book_1_html = """
<div class="page_inner">
  <ul class="breadcrumb">
    <li><a href="../../index.html">Home</a></li>
    <li><a href="../category/books_1/index.html">Books</a></li>
    <li><a href="../category/books/poetry_23/index.html">Poetry</a></li>
    <li class="active">A Light in the Attic</li>
  </ul>

  <div id="messages"></div>

  <div class="content">
    <div id="promotions"></div>

    <div id="content_inner">
      <article class="product_page">
        <div class="row">
          <div class="col-sm-6">
            <div id="product_gallery" class="carousel">
              <div class="thumbnail">
                <div class="carousel-inner">
                  <div class="item active">
                    <img src="../../media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg" alt="A Light in the Attic">
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-sm-6 product_main">
            <h1>A Light in the Attic</h1>
            <p class="price_color">£51.77</p>
            <p class="instock availability"><i class="icon-ok"></i> In stock (22 available)</p>

            <p class="star-rating Three">
              <i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i>
              <!-- <small><a href="/catalogue/a-light-in-the-attic_1000/reviews/"> 0 customer reviews </a></small> -->&nbsp;
              <!-- <a id="write_review" href="/catalogue/a-light-in-the-attic_1000/reviews/add/#addreview" class="btn btn-success btn-sm">Write a review</a> -->
            </p>

            <hr>
            <div class="alert alert-warning" role="alert"><strong>Warning!</strong> This is a demo website for web scraping purposes. Prices and ratings here were randomly assigned and have no real meaning.</div>
          </div>
        </div>

        <div id="product_description" class="sub-header">
          <h2>Product Description</h2>
        </div>
        <p>It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love th It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love that Silverstein. Need proof of his genius? RockabyeRockabye baby, in the treetopDon't you know a treetopIs no safe place to rock?And who put you up there,And your cradle, too?Baby, I think someone down here'sGot it in for you. Shel, you never sounded so good. ...more</p>

        <div class="sub-header">
          <h2>Product Information</h2>
        </div>
        <table class="table table-striped">          
            <tr><th>UPC</th><td>a897fe39b1053632</td></tr>
            <tr><th>Product Type</th><td>Books</td></tr>
            <tr><th>Price (excl. tax)</th><td>£51.77</td></tr>
            <tr><th>Price (incl. tax)</th><td>£52.97</td></tr>
            <tr><th>Tax</th><td>£1.20</td></tr>
            <tr><th>Availability</th><td>In stock (22 available)</td></tr>
            <tr><th>Number of reviews</th><td>0</td></tr>          
        </table>

        <section>
          <div id="reviews" class="sub-header"></div>
        </section>
      </article>
    </div>
  </div>
</div>
"""

content_page_1_book_2_html = """
<div class="page_inner">
  <ul class="breadcrumb">
    <li><a href="../../index.html">Home</a></li>
    <li><a href="../category/books_1/index.html">Books</a></li>
    <li><a href="../category/books/historical-fiction_4/index.html">Historical Fiction</a></li>
    <li class="active">Tipping the Velvet</li>
  </ul>

  <div id="messages"></div>

  <div class="content">
    <div id="promotions"></div>

    <div id="content_inner">
      <article class="product_page">
        <div class="row">
          <div class="col-sm-6">
            <div id="product_gallery" class="carousel">
              <div class="thumbnail">
                <div class="carousel-inner">
                  <div class="item active">
                    <img src="../../media/cache/08/e9/08e94f3731d7d6b760dfbfbc02ca5c62.jpg" alt="Tipping the Velvet">
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-sm-6 product_main">
            <h1>Tipping the Velvet</h1>
            <p class="price_color">£53.74</p>
            <p class="instock availability"><i class="icon-ok"></i> In stock (20 available)</p>
            <p class="star-rating One">
              <i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i>
              <!-- <small><a href="/catalogue/tipping-the-velvet_999/reviews/"> 0 customer reviews </a></small> -->&nbsp;
              <!-- <a id="write_review" href="/catalogue/tipping-the-velvet_999/reviews/add/#addreview" class="btn btn-success btn-sm">Write a review</a> -->
            </p>
            <hr>
            <div class="alert alert-warning" role="alert"><strong>Warning!</strong> This is a demo website for web scraping purposes. Prices and ratings here were randomly assigned and have no real meaning.</div>
          </div>
        </div>

        <div id="product_description" class="sub-header"><h2>Product Description</h2></div>        

        <div class="sub-header"><h2>Product Information</h2></div>
        <table class="table table-striped">
          <tbody>
            <tr><th>UPC</th><td>90fa61229261140a</td></tr>
            <tr><th>Product Type</th><td>Books</td></tr>
            <tr><th>Price (excl. tax)</th><td>£53.74</td></tr>
            <tr><th>Price (incl. tax)</th><td>£53.74</td></tr>
            <tr><th>Tax</th><td>£0.00</td></tr>
            <tr><th>Availability</th><td>In stock (20 available)</td></tr>
            <tr><th>Number of reviews</th><td>2</td></tr>
          </tbody>
        </table>

        <section><div id="reviews" class="sub-header"></div></section>

        <div class="sub-header"><h2>Products you recently viewed</h2></div>
        <ul class="row">
          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../a-light-in-the-attic_1000/index.html"><img src="../../media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg" alt="A Light in the Attic" class="thumbnail"></a>
              </div>
              <p class="star-rating Three">
                <i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i>
              </p>
              <h3><a href="../a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a></h3>
              <div class="product_price">
                <p class="price_color">£51.77</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>
        </ul>
      </article>
    </div>
  </div>
</div>
"""

content_page_2_book_1_html = """
<div class="page_inner">
  <ul class="breadcrumb">
    <li><a href="../../index.html">Home</a></li>
    <li><a href="../category/books_1/index.html">Books</a></li>
    <li><a href="../category/books/default_15/index.html">Default</a></li>
    <li class="active">Frankenstein</li>
  </ul>

  <div id="messages"></div>

  <div class="content">
    <div id="promotions"></div>

    <div id="content_inner">
      <article class="product_page">
        <div class="row">
          <div class="col-sm-6">
            <div id="product_gallery" class="carousel">
              <div class="thumbnail">
                <div class="carousel-inner">
                  <div class="item active">
                    <img src="../../media/cache/f7/22/f722c24607ddc8013476ca8e84639ba7.jpg" alt="Frankenstein">
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-sm-6 product_main">
            <h1>Frankenstein</h1>
            <p class="price_color">£38.00</p>
            <p class="instock availability"><i class="icon-ok"></i> In stock (1 available)</p>
            <p class="star-rating Two">
              <i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i>
              <!-- <small><a href="/catalogue/frankenstein_20/reviews/">0 customer reviews</a></small> -->&nbsp;
              <!-- <a id="write_review" href="/catalogue/frankenstein_20/reviews/add/#addreview" class="btn btn-success btn-sm">Write a review</a> -->
            </p>
            <hr>
            <div class="alert alert-warning" role="alert"><strong>Warning!</strong> This is a demo website for web scraping purposes. Prices and ratings here were randomly assigned and have no real meaning.</div>
          </div>
        </div>

        <div id="product_description" class="sub-header"><h2>Product Description</h2></div>
        <p></p>

        <div class="sub-header"><h2>Product Information</h2></div>
        <table class="table table-striped">
          <tbody>
            <tr><th>UPC</th><td>a492f49a3e2b6a71</td></tr>
            <tr><th>Product Type</th><td>Books</td></tr>
            <tr><th>Price (excl. tax)</th><td>£38.00</td></tr>
            <tr><th>Price (incl. tax)</th><td>£38.00</td></tr>
            <tr><th>Tax</th><td>£0.00</td></tr>
            <tr><th>Availability</th><td>In stock (1 available)</td></tr>
            <tr><th>Number of reviews</th><td>3</td></tr>
          </tbody>
        </table>

        <section><div id="reviews" class="sub-header"></div></section>

        <div class="sub-header"><h2>Products you recently viewed</h2></div>
        <ul class="row">
          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../jane-eyre_27/index.html"><img src="../../media/cache/0b/9b/0b9bd2c1de5ec402b2c797b53e5257f6.jpg" alt="Jane Eyre" class="thumbnail"></a>
              </div>
              <p class="star-rating Five"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../jane-eyre_27/index.html" title="Jane Eyre">Jane Eyre</a></h3>
              <div class="product_price">
                <p class="price_color">£38.43</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>

          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../on-the-road-duluoz-legend_40/index.html"><img src="../../media/cache/b8/3e/b83e5f1b9c1dcfe0ef05cff4b080e0fa.jpg" alt="On the Road (Duluoz Legend)" class="thumbnail"></a>
              </div>
              <p class="star-rating Three"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../on-the-road-duluoz-legend_40/index.html" title="On the Road (Duluoz Legend)">On the Road (Duluoz ...)</a></h3>
              <div class="product_price">
                <p class="price_color">£32.36</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>

          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../paradise-lost-paradise-1_45/index.html"><img src="../../media/cache/66/f9/66f9edebe41032584e08dcf2fc27b8b4.jpg" alt="Paradise Lost (Paradise #1)" class="thumbnail"></a>
              </div>
              <p class="star-rating One"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../paradise-lost-paradise-1_45/index.html" title="Paradise Lost (Paradise #1)">Paradise Lost (Paradise #1)</a></h3>
              <div class="product_price">
                <p class="price_color">£24.96</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>

          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../shatter-me-shatter-me-1_53/index.html"><img src="../../media/cache/f0/31/f031254cafbdff0092c76c8dcba24139.jpg" alt="Shatter Me (Shatter Me #1)" class="thumbnail"></a>
              </div>
              <p class="star-rating One"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../shatter-me-shatter-me-1_53/index.html" title="Shatter Me (Shatter Me #1)">Shatter Me (Shatter Me ...)</a></h3>
              <div class="product_price">
                <p class="price_color">£42.40</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>

          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../taking-shots-assassins-1_57/index.html"><img src="../../media/cache/ea/92/ea92404bce04a4bc76f3ed9c5344b2bf.jpg" alt="Taking Shots (Assassins #1)" class="thumbnail"></a>
              </div>
              <p class="star-rating Two"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../taking-shots-assassins-1_57/index.html" title="Taking Shots (Assassins #1)">Taking Shots (Assassins #1)</a></h3>
              <div class="product_price">
                <p class="price_color">£18.88</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>

          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../the-name-of-the-wind-the-kingkiller-chronicle-1_74/index.html"><img src="../../media/cache/6a/b3/6ab3616e7495ef64b1546a178cf8a9e7.jpg" alt="The Name of the Wind (The Kingkiller Chronicle #1)" class="thumbnail"></a>
              </div>
              <p class="star-rating Three"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../the-name-of-the-wind-the-kingkiller-chronicle-1_74/index.html" title="The Name of the Wind (The Kingkiller Chronicle #1)">The Name of the ...</a></h3>
              <div class="product_price">
                <p class="price_color">£50.59</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>
        </ul>
      </article>
    </div>
  </div>
</div>
"""

content_page_2_book_2_html = """
<div class="page_inner">
  <ul class="breadcrumb">
    <li><a href="../../index.html">Home</a></li>
    <li><a href="../category/books_1/index.html">Books</a></li>
    <li><a href="../category/books/music_14/index.html">Music</a></li>
    <li class="active">Forever Rockers (The Rocker #12)</li>
  </ul>

  <div id="messages"></div>

  <div class="content">
    <div id="promotions"></div>

    <div id="content_inner">
      <article class="product_page">
        <div class="row">
          <div class="col-sm-6">
            <div id="product_gallery" class="carousel">
              <div class="thumbnail">
                <div class="carousel-inner">
                  <div class="item active">
                    <img src="../../media/cache/a2/fc/a2fc91793502f5c10b5826ad606de435.jpg" alt="Forever Rockers (The Rocker #12)">
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-sm-6 product_main">
            <h1>Forever Rockers (The Rocker #12)</h1>
            <p class="price_color">£28.80</p>
            <p class="instock availability"><i class="icon-ok"></i> In stock (1 available)</p>
            <p class="star-rating Three">
              <i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i>
              <!-- <small><a href="/catalogue/forever-rockers-the-rocker-12_19/reviews/">0 customer reviews</a></small> -->&nbsp;
              <!-- <a id="write_review" href="/catalogue/forever-rockers-the-rocker-12_19/reviews/add/#addreview" class="btn btn-success btn-sm">Write a review</a> -->
            </p>
            <hr>
            <div class="alert alert-warning" role="alert"><strong>Warning!</strong> This is a demo website for web scraping purposes. Prices and ratings here were randomly assigned and have no real meaning.</div>
          </div>
        </div>

        <div id="product_description" class="sub-header"><h2>Product Description</h2></div>
        <p>My Happily Ever After was turning into a living nightmare... All I wanted was Harper's happiness and I would move the world to give her anything she ever wanted. We've searched for answers, talked about our options, and finally-FINALLY-found hope. Yet, just when things seemed to be perfect, it all came crashing down around us all. The one person I've always counted on to h My Happily Ever After was turning into a living nightmare... All I wanted was Harper's happiness and I would move the world to give her anything she ever wanted. We've searched for answers, talked about our options, and finally-FINALLY-found hope. Yet, just when things seemed to be perfect, it all came crashing down around us all. The one person I've always counted on to hold us together-to hold me together-was lost in her own nightmares and I felt like I was losing everything. Everything. I wasn't going to lose the woman I loved. I would hold onto her until the last breath left my body. It was my mistakes that were hurting us and I would be the one to fix it. I wouldn't let my past ruin my forever with Harper. ...more</p>

        <div class="sub-header"><h2>Product Information</h2></div>
        <table class="table table-striped">
          <tbody>
            <tr><th>UPC</th><td>e564c3f1a93ccf2e</td></tr>
            <tr><th>Product Type</th><td>Books</td></tr>
            <tr><th>Price (excl. tax)</th><td>£28.80</td></tr>
            <tr><th>Price (incl. tax)</th><td>£28.80</td></tr>
            <tr><th>Tax</th><td>£0.00</td></tr>
            <tr><th>Availability</th><td>In stock (1 available)</td></tr>
            <tr><th>Number of reviews</th><td>4</td></tr>
          </tbody>
        </table>

        <section><div id="reviews" class="sub-header"></div></section>

        <div class="sub-header"><h2>Products you recently viewed</h2></div>
        <ul class="row">
          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../old-records-never-die-one-mans-quest-for-his-vinyl-and-his-past_39/index.html"><img src="../../media/cache/7e/94/7e947f3dd04f178175b85123829467a9.jpg" alt="Old Records Never Die: One Man's Quest for His Vinyl and His Past" class="thumbnail"></a>
              </div>
              <p class="star-rating Two"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../old-records-never-die-one-mans-quest-for-his-vinyl-and-his-past_39/index.html" title="Old Records Never Die: One Man's Quest for His Vinyl and His Past">Old Records Never Die: ...</a></h3>
              <div class="product_price">
                <p class="price_color">£55.66</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>

          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../life_104/index.html"><img src="../../media/cache/99/97/9997eda658c2fe50e724171f9c2a2b0b.jpg" alt="Life" class="thumbnail"></a>
              </div>
              <p class="star-rating Five"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../life_104/index.html" title="Life">Life</a></h3>
              <div class="product_price">
                <p class="price_color">£31.58</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>

          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../no-one-here-gets-out-alive_336/index.html"><img src="../../media/cache/7a/7e/7a7eb52e7075a5305522948375c1316e.jpg" alt="No One Here Gets Out Alive" class="thumbnail"></a>
              </div>
              <p class="star-rating Five"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../no-one-here-gets-out-alive_336/index.html" title="No One Here Gets Out Alive">No One Here Gets ...</a></h3>
              <div class="product_price">
                <p class="price_color">£20.02</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>

          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../orchestra-of-exiles-the-story-of-bronislaw-huberman-the-israel-philharmonic-and-the-one-thousand-jews-he-saved-from-nazi-horrors_337/index.html"><img src="../../media/cache/15/de/15de75548ee9a4c6be1420ee309c03e0.jpg" alt="Orchestra of Exiles: The Story of Bronislaw Huberman, the Israel Philharmonic, and the One Thousand Jews He Saved from Nazi Horrors" class="thumbnail"></a>
              </div>
              <p class="star-rating Three"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../orchestra-of-exiles-the-story-of-bronislaw-huberman-the-israel-philharmonic-and-the-one-thousand-jews-he-saved-from-nazi-horrors_337/index.html" title="Orchestra of Exiles: The Story of Bronislaw Huberman, the Israel Philharmonic, and the One Thousand Jews He Saved from Nazi Horrors">Orchestra of Exiles: The ...</a></h3>
              <div class="product_price">
                <p class="price_color">£12.36</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>

          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../this-is-your-brain-on-music-the-science-of-a-human-obsession_414/index.html"><img src="../../media/cache/35/a4/35a4a7c6c76c4e82186753078e441654.jpg" alt="This Is Your Brain on Music: The Science of a Human Obsession" class="thumbnail"></a>
              </div>
              <p class="star-rating One"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../this-is-your-brain-on-music-the-science-of-a-human-obsession_414/index.html" title="This Is Your Brain on Music: The Science of a Human Obsession">This Is Your Brain ...</a></h3>
              <div class="product_price">
                <p class="price_color">£38.40</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>

          <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
            <article class="product_pod">
              <div class="image_container">
                <a href="../chronicles-vol-1_462/index.html"><img src="../../media/cache/11/fc/11fc94453c4dc0d68543971d7843afb0.jpg" alt="Chronicles, Vol. 1" class="thumbnail"></a>
              </div>
              <p class="star-rating Two"><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i><i class="icon-star"></i></p>
              <h3><a href="../chronicles-vol-1_462/index.html" title="Chronicles, Vol. 1">Chronicles, Vol. 1</a></h3>
              <div class="product_price">
                <p class="price_color">£52.60</p>
                <p class="instock availability"><i class="icon-ok"></i> In stock</p>
                <form><button type="submit" class="btn btn-primary btn-block" data-loading-text="Adding...">Add to basket</button></form>
              </div>
            </article>
          </li>
        </ul>
      </article>
    </div>
  </div>
</div>

"""


class ScraperBookUtilsMock(Static):

    @classmethod
    def mock_http_books_to_scrape_valid(cls, http_request_mock: respx.MockRouter) -> None:
        http_request_mock.get(host="books.toscrape.com", path="/").mock(
            return_value=cls._resp(page_1_html)
        )

        http_request_mock.get(host="books.toscrape.com", path="/catalogue/page-2.html").mock(
            return_value=cls._resp(page_2_html)
        )

        http_request_mock.get(
            host="books.toscrape.com", path="/catalogue/a-light-in-the-attic_1000/index.html"
        ).mock(return_value=cls._resp(content_page_1_book_1_html))

        http_request_mock.get(
            host="books.toscrape.com", path="/catalogue/tipping-the-velvet_999/index.html"
        ).mock(return_value=cls._resp(content_page_1_book_2_html))

        http_request_mock.get(
            host="books.toscrape.com", path="/catalogue/frankenstein_20/index.html"
        ).mock(return_value=cls._resp(content_page_2_book_1_html))

        http_request_mock.get(
            host="books.toscrape.com", path="/catalogue/forever-rockers-the-rocker-12_19/index.html"
        ).mock(return_value=cls._resp(content_page_2_book_2_html))

    @classmethod
    def mock_http_failed_load_site(cls, http_request_mock: respx.MockRouter) -> None:
        http_request_mock.get(host="books.toscrape.com", path="/").mock(
            return_value=cls._resp("""""", 404)
        )

    @classmethod
    def mock_http_failed_to_load_link(cls, http_request_mock: respx.MockRouter) -> None:
        http_request_mock.get(host="books.toscrape.com", path="/").mock(
            return_value=cls._resp(page_1_html)
        )

        http_request_mock.get(
            host="books.toscrape.com", path="/catalogue/a-light-in-the-attic_1000/index.html"
        ).mock(return_value=cls._resp("""""", 404))

    @classmethod
    def get_valid_books(cls, url: str, *args: Any, **kwargs: Any) -> httpx.Response:
        try:
            match url:
                case "https://books.toscrape.com":
                    return cls._resp(page_1_html)
                case "https://books.toscrape.com/catalogue/page-2.html":
                    return cls._resp(page_2_html)
                case "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html":
                    return cls._resp(content_page_1_book_1_html)
                case "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html":
                    return cls._resp(content_page_1_book_2_html)
                case "https://books.toscrape.com/catalogue/frankenstein_20/index.html":
                    return cls._resp(content_page_2_book_1_html)
                case "https://books.toscrape.com/catalogue/forever-rockers-the-rocker-12_19/index.html":
                    return cls._resp(content_page_2_book_2_html)
                case _:
                    raise KeyError
        except KeyError:
            return cls._resp("""not found""", 404)

    @classmethod
    def invalid_books(cls, url: str, *args: Any, **kwargs: Any) -> httpx.Response:
        return cls._resp("""""", 404)

    @classmethod
    def invalid_link_book(cls, url: str, *args: Any, **kwargs: Any) -> httpx.Response:
        try:
            match url:
                case "https://books.toscrape.com":
                    return cls._resp(page_1_html)
                case "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html":
                    return cls._resp("""""", 404)
                case _:
                    raise KeyError
        except KeyError:
            return httpx.Response(404, content="""not found""")

    @classmethod
    def scraped_books(cls) -> list[ScrapeBook]:
        return [
            ScrapeBook(
                category="Poetry",
                title="A Light in the Attic",
                rating=Rating(3),
                product_description="It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love th It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love that Silverstein. Need proof of his genius? RockabyeRockabye baby, in the treetopDon't you know a treetopIs no safe place to rock?And who put you up there,And your cradle, too?Baby, I think someone down here'sGot it in for you. Shel, you never sounded so good. ...more",
                upc=Upc("a897fe39b1053632"),
                product_type="Books",
                price_full=Money.from_float(52.97),
                price_excl_tax=Money.from_float(51.77),
                tax=Money.from_float(1.20),
                availability=22,
                number_reviews=0,
                image_url="https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg",
                product_page_url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
                model_id=1,
            ),
            ScrapeBook(
                category="Historical Fiction",
                title="Tipping the Velvet",
                rating=Rating(1),
                product_description="",
                upc=Upc("90fa61229261140a"),
                product_type="Books",
                price_full=Money.from_float(53.74),
                price_excl_tax=Money.from_float(53.74),
                tax=Money.from_float(0),
                availability=20,
                number_reviews=2,
                image_url="https://books.toscrape.com/media/cache/08/e9/08e94f3731d7d6b760dfbfbc02ca5c62.jpg",
                product_page_url="https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
                model_id=2,
            ),
            ScrapeBook(
                category="Default",
                title="Frankenstein",
                rating=Rating(2),
                product_description="",
                upc=Upc("a492f49a3e2b6a71"),
                product_type="Books",
                price_full=Money.from_float(38.00),
                price_excl_tax=Money.from_float(38.00),
                tax=Money.from_float(0),
                availability=1,
                number_reviews=3,
                image_url="https://books.toscrape.com/media/cache/f7/22/f722c24607ddc8013476ca8e84639ba7.jpg",
                product_page_url="https://books.toscrape.com/catalogue/frankenstein_20/index.html",
                model_id=3,
            ),
            ScrapeBook(
                category="Music",
                title="Forever Rockers (The Rocker #12)",
                rating=Rating(3),
                product_description="My Happily Ever After was turning into a living nightmare... All I wanted was Harper's happiness and I would move the world to give her anything she ever wanted. We've searched for answers, talked about our options, and finally-FINALLY-found hope. Yet, just when things seemed to be perfect, it all came crashing down around us all. The one person I've always counted on to h My Happily Ever After was turning into a living nightmare... All I wanted was Harper's happiness and I would move the world to give her anything she ever wanted. We've searched for answers, talked about our options, and finally-FINALLY-found hope. Yet, just when things seemed to be perfect, it all came crashing down around us all. The one person I've always counted on to hold us together-to hold me together-was lost in her own nightmares and I felt like I was losing everything. Everything. I wasn't going to lose the woman I loved. I would hold onto her until the last breath left my body. It was my mistakes that were hurting us and I would be the one to fix it. I wouldn't let my past ruin my forever with Harper. ...more",
                upc=Upc("e564c3f1a93ccf2e"),
                product_type="Books",
                price_full=Money.from_float(28.80),
                price_excl_tax=Money.from_float(28.80),
                tax=Money.from_float(0),
                availability=1,
                number_reviews=4,
                image_url="https://books.toscrape.com/media/cache/a2/fc/a2fc91793502f5c10b5826ad606de435.jpg",
                product_page_url="https://books.toscrape.com/catalogue/forever-rockers-the-rocker-12_19/index.html",
                model_id=4,
            ),
        ]

    @classmethod
    def _resp(cls, html: str, status: int = 200) -> httpx.Response:
        return httpx.Response(status, content=html)
