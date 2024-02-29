package br.com.apaschoalon.services;

import java.util.concurrent.atomic.AtomicLong;
import java.util.logging.Logger;

import org.springframework.stereotype.Service;

import model.Person;

@Service
public class PersonServices {

	private final AtomicLong counter = new AtomicLong();
	
	private Logger logger = Logger.getLogger(PersonServices.class.getName());
	
	public Person findById(String id) {
		
		logger.info("Finding one person...");
		Person person = new Person();
		person.setId(this.counter.getAndIncrement());
		person.setFirstName("Leandro");
		person.setLastName("Costa");
		person.setAddress("Valinhos");
		person.setGender("Male");
		
		return person;
	}
	
}
