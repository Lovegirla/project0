all:
	mkdir ./workspace
	mkdir -p ./evaluation/input
	mkdir -p ./evaluation/output
	python3 ./utils/convert_circuits.py -c usb_phy
	python3 ./symcts/flow.py
	cp ./utils/extract.pl ./workspace
	cp ./utils/view.pl ./workspace
	cp ./utils/evaluation.py ./workspace
	cp ./evaluation/input/usb_phy ./workspace
	cp ./evaluation/output/result ./workspace
	cp ./library/tech/45nm_LP.pm ./workspace
	cp ./library/spice/* ./workspace
	cd workspace
	./extract.pl usb_phy result 45nm_LP
clean:
	rm -rf workspace
	rm -rf ./evaluation/input
	rm -rf ./evaluation/output
