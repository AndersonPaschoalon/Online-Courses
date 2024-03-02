package br.com.apaschoalon.services;

import java.util.List;
import java.util.logging.Logger;

import org.hibernate.ResourceClosedException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import br.com.apaschoalon.data.vo.v1.PersonVO;
import br.com.apaschoalon.mapper.DozerMapper;
import br.com.apaschoalon.model.Person;
import br.com.apaschoalon.repositories.PersonRepository;

@Service
public class PersonServices {

	// private final AtomicLong counter = new AtomicLong();
	
	private Logger logger = Logger.getLogger(PersonServices.class.getName());
	
	@Autowired
	PersonRepository repository;
	
	public PersonVO findById(Long id) {
		logger.info("Finding one person...");
		var entity = this.repository.findById(id)
				.orElseThrow(() -> new ResourceClosedException("No records found for this ID: " + id));
		return DozerMapper.parseObject(entity, PersonVO.class);
	}
	
	public List<PersonVO> findAll() {
		logger.info("Finding all people...");
		return DozerMapper.parseListObjects(this.repository.findAll(), PersonVO.class);
	}

	public PersonVO create(PersonVO person) {
		logger.info("Creating one person!");
		var entity = DozerMapper.parseObject(person, Person.class);
		
		var savedPerson  = this.repository.save(entity);
		var vo = DozerMapper.parseObject(savedPerson, PersonVO.class);
		return vo;
	}	

	public PersonVO update(PersonVO person) {
		logger.info("Creating one person!");
		
		var entity = this.repository.findById(person.getId())
				.orElseThrow(() -> new ResourceClosedException("No records found for this ID: " + person.getId()));
		
		entity.setFirstName(person.getFirstName());
		entity.setLastName(person.getLastName());
		entity.setAddress(person.getAddress());
		entity.setGender(person.getGender());		
		
		var savedPerson  = this.repository.save(entity);
		var vo = DozerMapper.parseObject(savedPerson, PersonVO.class);
		return vo;
	}	
	
	public void delete(Long id) {
		logger.info("Deleting one person!");
		var entity = this.repository.findById(id)
				.orElseThrow(() -> new ResourceClosedException("No records found for this ID: " + id));
		this.repository.delete(entity);
	}	
	
	// private Person mockPerson(int i) {
	// 
	// 	Person person = new Person();
	// 	person.setId(this.counter.getAndIncrement());
	// 	person.setFirstName("Person Name " + i);
	// 	person.setLastName("Last Name " + i);
	// 	person.setAddress("Adress " + i);
	// 	person.setGender("Male");
	// 	
	// 	return person;
	// }	


	
}
