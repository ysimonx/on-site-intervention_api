
photos_src=/var/www/html/api_renovadmin/app/static/photos
timestamps_dest=/var/www/html/api_renovadmin/app/static/photos/timestamps

mkdir -p $timestamps_dest

cd $photos_src
for filename in *; do
 
    if [ "$filename" == "timestamps" ]; then
       continue
    else
        # echo "File -> $filename"
        filename_sig="$timestamps_dest/$filename.digicert.tsr.txt"
        if [ -f "$filename_sig" ]; then
            continue
        else
            echo "Signature n'existe pas encore : $filename_sig"
            input_file=$filename
	    
	    # timestamp digicert

            openssl ts -query -data $input_file -no_nonce -sha512 -cert -out /tmp/$input_file.digicert.tsq
	        curl -H "Content-Type: application/timestamp-query" --data-binary "@/tmp/$input_file.digicert.tsq"  http://timestamp.digicert.com > /tmp/$input_file.digicert.tsr
            openssl ts -reply -in /tmp/$input_file.digicert.tsr -text > /tmp/$input_file.digicert.tsr.txt

            mv "/tmp/$input_file.digicert.tsq" $timestamps_dest/
            mv "/tmp/$input_file.digicert.tsr" $timestamps_dest/
            mv "/tmp/$input_file.digicert.tsr.txt" $timestamps_dest/


	# timestamp certigna
        # cf : horodatage.certigna.com
        # user : yannick.simon@kysoe.com
        # password : zfuU9!&Mc%7x3^FT
        
        #    openssl ts -query -data $input_file -no_nonce -sha512 -cert -out /tmp/$input_file.certigna.tsq
	#    curl -H "Content-Type: application/timestamp-query" --user "d73cf663:ba8b678b12fc" --data-binary "@/tmp/$input_file.certigna.tsq" https://timestamp.dhimyotis.com/api/v1/ > /tmp/$input_file.certigna.tsr
        #    openssl ts -reply -in /tmp/$input_file.certigna.tsr -text > /tmp/$input_file.certigna.tsr.txt

	#    mv "/tmp/$input_file.certigna.tsq" $timestamps_dest/
        #    mv "/tmp/$input_file.certigna.tsr" $timestamps_dest/
        #    mv "/tmp/$input_file.certigna.tsr.txt" $timestamps_dest/

	    
        fi

    fi

done
