resultFile = "/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/results/results9.csv";
answerFile = "/media/mihir/E6DEBC2BDEBBF243/MEng folders/NLP/Project3/data_sets/answer_set_2";

def getFileHandler(fileName):
	return open(fileName);

def getFileHandlerForWrite(fileName):
	return open(fileName,"w+");

def modelEfficiencyCalculator(resultFile,answerFile):
	resultFileHandler = getFileHandler(resultFile);
	answerFileHandler = getFileHandler(answerFile);
	#print( resultFile)
	result = {};
	result['PER'] = [];
	result['ORG'] = [];
	result['LOC'] = [];
	result['MISC'] = [];

	answer = {};
	answer['PER'] = [];
	answer['ORG'] = [];
	answer['LOC'] = [];
	answer['MISC'] = [];
	counter = 0;
	while(True):
		statement =  resultFileHandler.readline();
		if not statement:
			break;
		counter += 1;
		#print statement;
		if(counter == 1):
			continue;
		
		#print "hello" + statement;
		tag_result = statement.split(",");
		print("tag_result="+str(tag_result));
		indexes = tag_result[1].split();
		result[tag_result[0]].extend(indexes);	

	counter = 0;

	while(True):
		statement =  answerFileHandler.readline();
		#print statement;
		if not statement:
			break;
		counter += 1;
		if(counter == 1):
			continue;
		counter+=1;
		tag_result = statement.split(",");
		indexes = tag_result[1].split();
		answer[tag_result[0]].extend(indexes);	

	#print answer
	#print result

	correct_predictions = 0;
	total_predictions = 0;
	for key in result:
		total_predictions+=len(result[key]);
		for prediction in result[key]:
			if prediction in answer[key]:
				correct_predictions+=1;

	total_actual_predictions = 0;
	for key in answer:
		total_actual_predictions+=len(answer[key]);
	precision = (correct_predictions * 1.0) / total_predictions;
	recall = (correct_predictions * 1.0) / total_actual_predictions;
	fmeasure = (2 * precision * recall) / (precision + recall);
	print (precision,recall,fmeasure);

modelEfficiencyCalculator(resultFile, answerFile)