echo "Downloading Geonames gazetteer..."
curl -o allCountries.zip http://download.geonames.org/export/dump/allCountries.zip
echo "Unpacking Geonames gazetteer..."
unzip allCountries.zip

echo "Creating mappings for the fields in the Geonames index..."
curl -XPUT 'localhost:9200/geonames' -H 'Content-Type: application/json' -d @geonames_mapping.json

echo "Loading gazetteer into Elasticsearch..."
python3 geonames_elasticsearch_loader.py

echo "Done"
