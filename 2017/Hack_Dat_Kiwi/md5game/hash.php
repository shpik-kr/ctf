<?php
  for($i=0;$i<1000000000;$i++){
    $p= '0e'.intval($i);
    if(md5($p)==$p){
      echo $i;
      break;
    }
  }
?>
