<!DOCTYPE html>
<html>
    
    <head>
        <?php require_once("include/head.php")?>
        <?php require_once("config.php")?>
    </head>
    <body>
        <?php require_once("include/header.php")?>
            
        <!--================End Main Header Area =================-->
        <section class="banner_area our-products">
			<div class="banner_inner_area">
				<div class="container">
					<div class="banner_text text-left">
						<h3>Our Menu</h3>
						<ul>
							<li><a href="index.php">Home</a></li>
							<li><a href="menu.php">Our Menu</a></li>
						</ul>
					</div>
				</div>
			</div>
        </section>
        <!--================End Main Header Area =================-->
        <!--================Product Area =================-->
      
       
        <section class="product_area p_100">
        	<div class="container">
        		<div class="row product_inner_row">
        			<div class="col-lg-12">
        				<div class="row m0 product_task_bar"> 
							<div class="product_task_inner"> 
								<div class="float-left">
									<span>Showing 1 - 10 of 55 results</span>
								</div>
								<div class="float-right">
									<h4>Sort by :</h4>
									<select class="short">
										<option data-display="Default">Default</option>
										<option value="1">Default</option>
										<option value="2">Default</option>
										<option value="4">Default</option>
									</select>
								</div>
							</div>
        				</div>
        				<div class="row product_item_inner">
        				    <?php  
        				    $result=mysqli_query($con,"SELECT * FROM tbl_product WHERE Status='1' ORDER BY pid");
        				    if(mysqli_num_rows($result) > 0){
        				    while($row=mysqli_fetch_array($result)){
        				    ?>
        					<div class="col-lg-3 col-md-4 col-6">
        						<div class="cake_feature_item">
									<a href="single-product.php?pid=<?php echo $row['pid'] ?>" class="cake_img d-block">
										<img src="img/product/<?php echo $row['image1'];  ?>" alt="">
									</a>
									<div class="cake_text">
										<!--<h4>$29</h4>-->
										<h3><a href="single-product.php?pid=<?php echo $row['pid'] ?>"><?php echo $row['productname'];  ?></a></h3>
										<!--<p>(Gold)</p>-->
										<!--<a class="pest_btn" href="#">Add to cart</a>-->
									</div>
								</div>
        					</div>
        					<?php }} ?>
        				</div>
       
        			</div>
        		</div>
        	</div>
        </section>
        <!--================End Product Area =================-->
        <?php require_once("include/footer.php")?>

    </body>
</html>